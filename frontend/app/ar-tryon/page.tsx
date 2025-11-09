'use client'

import { useState } from 'react'

export default function ARTryOnPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string>('')
  const [processing, setProcessing] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      
      // Create preview
      const reader = new FileReader()
      reader.onload = (e) => {
        setPreview(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleProcess = async () => {
    if (!selectedFile) return
    
    setProcessing(true)
    
    // Simulate AR processing
    setTimeout(() => {
      setResult({
        fit_score: 85,
        fit_category: 'good',
        recommendations: ['Consider size M for best fit'],
        processing_time: 4.2
      })
      setProcessing(false)
    }, 3000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold">AR Virtual Try-On</h1>
            <div className="flex gap-4">
              <a href="/" className="text-blue-600 hover:text-blue-700">
                Home
              </a>
              <a href="/products" className="text-blue-600 hover:text-blue-700">
                Products
              </a>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          {/* Instructions */}
          <div className="bg-blue-50 border-l-4 border-blue-500 p-6 mb-8">
            <h2 className="font-bold text-lg mb-2">How it works:</h2>
            <ol className="list-decimal list-inside space-y-2 text-gray-700">
              <li>Upload a full-body photo of yourself</li>
              <li>Select a clothing item to try on</li>
              <li>Our AI will detect your pose and overlay the clothing</li>
              <li>Get instant fit analysis and size recommendations</li>
            </ol>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Upload Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-6">Upload Your Photo</h2>
              
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                {preview ? (
                  <div className="space-y-4">
                    <img
                      src={preview}
                      alt="Preview"
                      className="max-h-64 mx-auto rounded-lg"
                    />
                    <button
                      onClick={() => {
                        setSelectedFile(null)
                        setPreview('')
                        setResult(null)
                      }}
                      className="text-red-600 hover:text-red-700"
                    >
                      Remove Photo
                    </button>
                  </div>
                ) : (
                  <>
                    <svg
                      className="mx-auto h-16 w-16 text-gray-400 mb-4"
                      stroke="currentColor"
                      fill="none"
                      viewBox="0 0 48 48"
                    >
                      <path
                        d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                        strokeWidth={2}
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                    <p className="text-gray-600 mb-4">
                      Click to upload or drag and drop
                    </p>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleFileSelect}
                      className="hidden"
                      id="file-upload"
                    />
                    <label
                      htmlFor="file-upload"
                      className="inline-block px-6 py-3 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700"
                    >
                      Choose Photo
                    </label>
                  </>
                )}
              </div>

              {selectedFile && !result && (
                <button
                  onClick={handleProcess}
                  disabled={processing}
                  className="mt-6 w-full py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400"
                >
                  {processing ? (
                    <span className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing...
                    </span>
                  ) : (
                    'Start AR Try-On'
                  )}
                </button>
              )}
            </div>

            {/* Results Section */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-6">Results</h2>
              
              {result ? (
                <div className="space-y-6">
                  <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <h3 className="font-bold text-lg mb-2">Fit Analysis</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>Fit Score:</span>
                        <span className="font-bold">{result.fit_score}/100</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Category:</span>
                        <span className="font-bold capitalize">{result.fit_category}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Processing Time:</span>
                        <span className="font-bold">{result.processing_time}s</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h3 className="font-bold text-lg mb-2">Recommendations</h3>
                    <ul className="list-disc list-inside space-y-1">
                      {result.recommendations.map((rec: string, idx: number) => (
                        <li key={idx} className="text-gray-700">{rec}</li>
                      ))}
                    </ul>
                  </div>

                  <button
                    onClick={() => {
                      setResult(null)
                      setSelectedFile(null)
                      setPreview('')
                    }}
                    className="w-full py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    Try Another Photo
                  </button>
                </div>
              ) : (
                <div className="text-center py-12 text-gray-500">
                  <svg className="mx-auto h-16 w-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p>Upload a photo to see results</p>
                </div>
              )}
            </div>
          </div>

          {/* Features */}
          <div className="mt-12 grid md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-xl shadow">
              <div className="text-4xl mb-3">🎯</div>
              <h3 className="font-bold mb-2">Pose Detection</h3>
              <p className="text-gray-600">Advanced AI detects 33 body landmarks for accurate overlay</p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow">
              <div className="text-4xl mb-3">📏</div>
              <h3 className="font-bold mb-2">Body Measurements</h3>
              <p className="text-gray-600">Automatically extract measurements from your photo</p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow">
              <div className="text-4xl mb-3">⚡</div>
              <h3 className="font-bold mb-2">Fast Processing</h3>
              <p className="text-gray-600">Get results in under 5 seconds</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
