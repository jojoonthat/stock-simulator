function PriceDisplay({ price }) {
  return (
    <p className="price-display">${price.toFixed(5)}</p>
  )
}

export default PriceDisplay;
