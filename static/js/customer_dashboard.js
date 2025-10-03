// Auto-refresh order status every 10 seconds
function refreshOrderStatus() {
    const orderRows = document.querySelectorAll('[data-order-id]');

    orderRows.forEach(async (statusElement) => {
        const orderId = statusElement.getAttribute('data-order-id');

        try {
            const response = await fetch(`/orders/api/${orderId}/`);
            if (response.ok) {
                const order = await response.json();

                // Update status badge
                let statusClass = '';
                if (order.status === 'pending') {
                    statusClass = 'bg-yellow-100 text-yellow-800';
                } else if (order.status === 'accepted') {
                    statusClass = 'bg-blue-100 text-blue-800';
                } else if (order.status === 'in_transit') {
                    statusClass = 'bg-purple-100 text-purple-800';
                } else if (order.status === 'delivered') {
                    statusClass = 'bg-green-100 text-green-800';
                } else if (order.status === 'cancelled') {
                    statusClass = 'bg-red-100 text-red-800';
                }

                statusElement.className = `px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${statusClass}`;
                statusElement.textContent = order.status.charAt(0).toUpperCase() + order.status.slice(1).replace('_', ' ');
            }
        } catch (error) {
            console.error('Error fetching order status:', error);
        }
    });
}

// Refresh every 10 seconds
if (document.getElementById('ordersTable')) {
    setInterval(refreshOrderStatus, 10000);
}
