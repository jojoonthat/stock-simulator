import { useState, useEffect } from "react";

function PriceDisplay() {
  const [currPrice, setCurrPrice] = useState(null)

  // Everytime page loads
  useEffect(() => {
    const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

    const refresh = async () => {
      while (true) {
        // Make GET req to flask server /next-tick endpoint
        // Parse response as json, yielding current price, and set state to current price
        const { curr_price } = await (await fetch("http://localhost:5000/next-tick")).json()
        setCurrPrice(curr_price);
        // Wait half a second before next iter
        await sleep(500);
      }
    }

    refresh()
  }, [])

  return (
    <p className="price-display">${currPrice?.toFixed(5)}</p>
  )
}

export default PriceDisplay;
