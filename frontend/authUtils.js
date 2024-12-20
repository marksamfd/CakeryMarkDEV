export const isUserPage = (url) =>
  url.startsWith('/customerOrders') ||
  url.startsWith('/customizeCake') ||
  url.startsWith('/checkout') ||
  url.startsWith('/cart');
export const isBakerPage = (url) => url.startsWith('/baker');
export const isAdminPage = (url) => url.startsWith('/admin');
export const isDeliveryPage = (url) => url.startsWith('/delivery');
