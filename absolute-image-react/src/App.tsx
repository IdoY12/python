import AbsoluteImage from "./components/absolute-image/AbsoluteImage"
import RelativeImage from "./components/relative-image/RelativeImage"
import "./App.css"

function App() {
  return (
    <div className="app">
      <div className="image-card">
        <AbsoluteImage />
      </div>
      <div className="image-card">
        <RelativeImage />
      </div>
    </div>
  )
}

export default App
