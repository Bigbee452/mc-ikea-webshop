// Function to render a single product
function renderCategory(category) {
    const categoryDiv = document.createElement('div');
    categoryDiv.className = 'category';

    categoryDiv.innerHTML = `
        <div class="col mb-5">
            <div class="card h-100">
                <!-- Product image-->
                <img class="card-img-top" src="assets/images/${category.image_url}" alt="..." />
                <!-- Product details-->
                <div class="card-body p-4">
                    <div class="text-center">
                        <!-- Product name (dirt)-->
                        <h5 class="fw-bolder">${category.name}</h5>
                    </div>
                </div>
                <!-- Product actions-->
                <div class="card-footer p-4 pt-0 border-top-0 bg-transparent">
                    <div class="text-center"><a class="btn btn-outline-dark mt-auto" href="#">View options</a></div>
                </div>
            </div>
        </div>
    `;

    return categoryDiv;
}

function renderProduct(product) {
    const productDiv = document.createElement('div');
    productDiv.className = 'product';

    productDiv.innerHTML = `
        <div class="col mb-5">
            <div class="card h-100">
                <!-- Product image-->
                <img class="card-img-top" src="assets/images/${product.image_url}" alt="..." />
                <!-- Product details-->
                <div class="card-body p-4">
                    <div class="text-center">
                        <!-- Product name (dirt)-->
                        <h5 class="fw-bolder">${product.name}</h5>
                        ${product.price} PPC / STACK
                    </div>
                </div>
                <!-- Product actions-->
                <div class="card-footer p-4 pt-0 border-top-0 bg-transparent">
                    <div class="text-center"><a class="btn btn-outline-dark mt-auto" href="#">Add to cart</a></div>
                </div>
            </div>
        </div>
    `;

    return productDiv;
}

  // Function to fetch and display all products
async function loadCategories() {
    try {
        const response = await fetch('http://192.168.0.254:7255/categories'); // Adjust URL if needed
        const categories = await response.json();
        const responseProducts = await fetch('http://192.168.0.254:7255/products'); // Adjust URL if needed
        const products = await responseProducts.json();

        const container = document.getElementById('products');
        container.innerHTML = ''; // Clear container

        categories.forEach(category => {
        container.appendChild(renderCategory(category));
        });
        products.forEach(product => {
        container.appendChild(renderProduct(product));
        });
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

window.addEventListener('DOMContentLoaded', loadCategories);