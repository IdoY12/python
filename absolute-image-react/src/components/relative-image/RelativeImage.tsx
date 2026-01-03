import beutiful_view from '../../images/beutiful_view.jpg'
import "./RelativeImage.css"

function RelativeImage() {
  return (
    <div className="relative-image">
      <h1>Relative Image:</h1>
      <img src={beutiful_view} alt="Beautiful View" />
    </div>
  )
}

export default RelativeImage