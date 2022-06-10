import { useState, useEffect } from "react";

function PriceDisplay() {
  const [currPrice, setCurrPrice] = useState(null)

  useEffect(() => {
    const sleep = ms => new Promise(resolve => setTimeout(resolve, ms))

    const refresh = async () => {
      while (true) {
        const { curr_price } = await (await fetch("http://localhost:5000/next-tick")).json()
        setCurrPrice(curr_price);
        await sleep(1000)
      }
    }

    refresh()
  }, [])

  return (
    <p className="price-display">${currPrice?.toFixed(5)}</p>
  )
}

export default PriceDisplay;
