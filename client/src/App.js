import { useState, useEffect } from "react"
import Slider from "./components/Slider";
import PriceDisplay from "./components/PriceDisplay";
import './App.css';

function App() {
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
    <div id="app">
      {currPrice &&
        <>
          <PriceDisplay price={currPrice}/>
          <Slider />
        </>
      }
    </div>
  );
}

export default App;
