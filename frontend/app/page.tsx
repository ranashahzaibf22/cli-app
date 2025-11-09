export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold text-gray-900 mb-6">
            StyleSense.AI
          </h1>
          <p className="text-2xl text-gray-600 mb-8">
            Virtual Fashion Try-On Platform
          </p>
          <p className="text-lg text-gray-500 max-w-2xl mx-auto mb-12">
            Experience the future of online shopping with AI-powered virtual try-on,
            pose detection, and personalized style recommendations.
          </p>
          
          <div className="flex gap-4 justify-center">
            <a
              href="/products"
              className="px-8 py-4 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Browse Products
            </a>
            <a
              href="/ar-tryon"
              className="px-8 py-4 bg-gray-200 text-gray-800 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
            >
              Try AR Now
            </a>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mt-16">
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="text-xl font-bold mb-3">Advanced AR Try-On</h3>
            <p className="text-gray-600">
              Real-time pose detection and realistic clothing overlay using MediaPipe technology
            </p>
          </div>

          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="text-xl font-bold mb-3">AI Recommendations</h3>
            <p className="text-gray-600">
              Personalized style suggestions powered by custom ML models and Groq AI
            </p>
          </div>

          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold mb-3">Fit Analysis</h3>
            <p className="text-gray-600">
              Accurate size recommendations based on body measurements and pose data
            </p>
          </div>
        </div>

        {/* Tech Stack */}
        <div className="mt-16 bg-white p-8 rounded-xl shadow-lg">
          <h2 className="text-3xl font-bold text-center mb-8">Powered By</h2>
          <div className="grid md:grid-cols-4 gap-6 text-center">
            <div>
              <p className="font-semibold text-lg">FastAPI</p>
              <p className="text-sm text-gray-600">Backend</p>
            </div>
            <div>
              <p className="font-semibold text-lg">Next.js 14</p>
              <p className="text-sm text-gray-600">Frontend</p>
            </div>
            <div>
              <p className="font-semibold text-lg">MediaPipe</p>
              <p className="text-sm text-gray-600">AR & Pose</p>
            </div>
            <div>
              <p className="font-semibold text-lg">TensorFlow</p>
              <p className="text-sm text-gray-600">ML Models</p>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="mt-16 grid md:grid-cols-4 gap-6 text-center">
          <div className="bg-blue-50 p-6 rounded-lg">
            <p className="text-4xl font-bold text-blue-600">500+</p>
            <p className="text-gray-700 mt-2">Fashion Items</p>
          </div>
          <div className="bg-blue-50 p-6 rounded-lg">
            <p className="text-4xl font-bold text-blue-600">4</p>
            <p className="text-gray-700 mt-2">ML Models</p>
          </div>
          <div className="bg-blue-50 p-6 rounded-lg">
            <p className="text-4xl font-bold text-blue-600">&lt;5s</p>
            <p className="text-gray-700 mt-2">AR Processing</p>
          </div>
          <div className="bg-blue-50 p-6 rounded-lg">
            <p className="text-4xl font-bold text-blue-600">90%+</p>
            <p className="text-gray-700 mt-2">Model Accuracy</p>
          </div>
        </div>
      </div>
    </main>
  )
}
