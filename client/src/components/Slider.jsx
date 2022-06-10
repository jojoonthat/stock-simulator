import { useState, useCallback } from "react";
import throttle from "lodash.throttle"

function Slider() {
  const [sliderVal, setSliderVal] = useState(5000);

  const setSentiment = newSentiment => {
    console.log("Send request!");
    newSentiment /= 10000
    fetch("http://localhost:5000/set-sentiment", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ newSentiment })
    })
  }

  // Disabling exhaustive-deps check because throttle is defined elsewhere
  const throttledRequest = useCallback(throttle(setSentiment, 200), []) // eslint-disable-line react-hooks/exhaustive-deps

  const handleChange = e => {
    setSliderVal(e.target.value)
    throttledRequest(e.target.value)
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
