/**
 * API Client for StyleSense.AI Backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiClient {
  private baseURL: string;
  private token: string | null;

  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Request failed' }));
        return { error: errorData.detail || `HTTP ${response.status}` };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('API request failed:', error);
      return { error: error instanceof Error ? error.message : 'Network error' };
    }
  }

  setToken(token: string) {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', token);
    }
  }

  clearToken() {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  }

  // Auth endpoints
  async register(email: string, username: string, password: string, full_name: string) {
    return this.request('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, username, password, full_name }),
    });
  }

  async login(username: string, password: string) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await this.request<{ access_token: string; token_type: string }>(
      '/api/v1/auth/login',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString(),
      }
    );

    if (response.data?.access_token) {
      this.setToken(response.data.access_token);
    }

    return response;
  }

  async getCurrentUser() {
    return this.request('/api/v1/auth/me');
  }

  // Product endpoints
  async getProducts(params?: { category?: string; skip?: number; limit?: number }) {
    const queryParams = new URLSearchParams();
    if (params?.category) queryParams.append('category', params.category);
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());

    const query = queryParams.toString();
    return this.request(`/api/v1/products${query ? `?${query}` : ''}`);
  }

  async getProduct(id: number) {
    return this.request(`/api/v1/products/${id}`);
  }

  async searchProducts(query: string) {
    return this.request('/api/v1/products/search', {
      method: 'POST',
      body: JSON.stringify({ query }),
    });
  }

  async getCategories() {
    return this.request('/api/v1/products/categories');
  }

  async getTrendingProducts() {
    return this.request('/api/v1/products/trending');
  }

  // AR endpoints
  async createARSession(clothing_item_id: number) {
    return this.request('/api/v1/ar/sessions', {
      method: 'POST',
      body: JSON.stringify({ clothing_item_id, session_type: 'photo' }),
    });
  }

  async uploadARImage(image: File, itemId: number) {
    const formData = new FormData();
    formData.append('file', image);
    formData.append('clothing_item_id', itemId.toString());

    const url = `${this.baseURL}/api/v1/ar/process`;
    const headers: HeadersInit = {};

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Upload failed' }));
        return { error: errorData.detail || `HTTP ${response.status}` };
      }

      const data = await response.json();
      return { data };
    } catch (error) {
      console.error('AR upload failed:', error);
      return { error: error instanceof Error ? error.message : 'Upload error' };
    }
  }

  async getARSessions() {
    return this.request('/api/v1/ar/sessions');
  }

  async analyzeFit(session_id: number) {
    return this.request('/api/v1/ar/analyze-fit', {
      method: 'POST',
      body: JSON.stringify({ session_id }),
    });
  }

  async rateARResult(session_id: number, rating: number, feedback?: string) {
    return this.request('/api/v1/ar/rate', {
      method: 'POST',
      body: JSON.stringify({ session_id, rating, feedback }),
    });
  }

  // ML endpoints
  async getMLModelsStatus() {
    return this.request('/api/v1/ml/models/status');
  }

  async predictSize(user_measurements: any, item_specs: any) {
    return this.request('/api/v1/ml/predict/size', {
      method: 'POST',
      body: JSON.stringify({ user_measurements, item_specs }),
    });
  }

  async predictStyle(items: any[]) {
    return this.request('/api/v1/ml/predict/style', {
      method: 'POST',
      body: JSON.stringify({ items }),
    });
  }

  async getRecommendations(user_id: number, limit?: number) {
    return this.request('/api/v1/ml/recommendations', {
      method: 'POST',
      body: JSON.stringify({ user_id, limit: limit || 10 }),
    });
  }
}

export const apiClient = new ApiClient();
export default apiClient;
