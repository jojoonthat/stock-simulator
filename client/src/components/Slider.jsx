import { useState } from "react";

function Slider() {
  const [sliderVal, setSliderVal] = useState(5000);

  const handleChange = e => {
    setSliderVal(e.target.value)
  }

  return (
    <div className="slider-container">
      <p>😨</p>
      <div className="slider">
        <input type="range" min={0} max={10000} value={sliderVal} onChange={handleChange} />
        <p>{sliderVal / 10000}</p>
      </div>
      <p>🤗</p>
    </div>
  )
}

export default Slider;
