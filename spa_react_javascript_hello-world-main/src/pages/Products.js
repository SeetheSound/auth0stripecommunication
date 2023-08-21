import React from 'react'

function Products() {
  return (
    <div>
<form action="/create-checkout-session" method="POST">
     

      <input type="hidden" name="priceId" value="price_1Ngr2AFVqhdR7gUTHNAbOFyq" />
      <button type="submit">Checkout</button>
    </form>
    </div>
  )
}

export default Products