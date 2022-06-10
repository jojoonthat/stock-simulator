import { useState, useCallback } from "react";
import throttle from "lodash.throttle"

function Slider() {
  // Slider default value starts at 5000, in the middle of the slider
  const [sliderVal, setSliderVal] = useState(5000);

  const setSentiment = newSentiment => {
    console.log("Send request!");
    // Dividing by 10000 because the sentiment scale ranges from 0 to 1
    newSentiment /= 10000
    // Send POST request and new sentiment value to server
    fetch("http://localhost:5000/set-sentiment", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ newSentiment })
    })
  }

  // Disabling exhaustive-deps check because throttle is defined elsewhere
  // Set sentiment with a 200ms throttle
  const throttledRequest = useCallback(throttle(setSentiment, 200), []) // eslint-disable-line react-hooks/exhaustive-deps

  // Fires when slider value changes: setSliderVal and send throttleRequest
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
