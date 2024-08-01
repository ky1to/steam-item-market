var global_id_page = 1
var selectedOption
let select_category = document.querySelector('#category')
var categorys = ['Hoodie', 'Road Sign Kilt', 'Jacket', 'Metal Facemask', 'Pants', 'Boots', 'Wood Storage Box', 'Large Wood Box', 'Baseball Cap', 'T-Shirt', 'Beenie Hat', 'Bandana Mask', 'Longsleeve T-Shirt', 'Snow Jacket', 'Improvised Balaclava', 'Hatchet', 'Roadsign Gloves', 'Road Sign Jacket', 'Coffee Can Helmet', 'Sheet Metal Door', 'Wooden Door', 'Rock', 'Garage Door', 'Custom SMG', 'Rug', 'Bolt Action Rifle', 'Pickaxe', 'Metal Chest Plate', 'Hide Poncho', 'Burlap Shoes', 'Furnace', 'Locker', 'Sheet Metal Double Door', 'Assault Rifle', 'Thompson', 'Semi-Automatic Rifle', 'L96 Rifle', 'Burlap Headwrap', 'Sleeping Bag', 'M249', 'Double Barrel Shotgun', 'Torch', 'Armored Door', 'Bone Helmet', 'MP5A4', 'Salvaged Sword', 
    'Boonie Hat', 'Semi-Automatic Pistol', 'Jackhammer', 'Wooden Spear', 'Rocket Launcher', 'Satchel Charge', 'Pump Shotgun', 'Hide Vest', 'Hunting Bow', 'Vending Machine', 'Hammer', 'Festive Window Garland', 'Crossbow', 'Armored Double Door', 'Python Revolver', 'Stone Hatchet', 'Stone Pickaxe', 'Bone Knife', 'Burlap Shirt', 'Leather Gloves', 'Burlap Trousers', 'Concrete Barricade', 'Riot Helmet', 'Hide Boots', 'Eoka Pistol', 'M39 Rifle', 'Hazmat Suit', 'Hide Pants', 'Reactive Target', 'Waterpipe Shotgun', 'Revolver', 'F1 Grenade', 'Shirt', 'Bucket Helmet', 'Combat Knife', 'Mace', 'Fridge', 'Hide Halterneck', 'Bone Club', 'Shorts', 'Wood Double Door', 'Chair', 'Water Purifier', 'Rug Bear Skin', 'Longsword', 'Salvaged Icepick', 'Table', 'Hide Skirt', 'Acoustic Guitar', 'Miners Hat']

get_request()

for(let option_category in categorys){
    let option = document.createElement('option');
    option.value = categorys[option_category]
    option.textContent = categorys[option_category]
    select_category.appendChild(option);
}

function update_html(data){
    if (global_id_page in [1,2,3,4,5]){
        for(let i = 1; i < 8; i++){
            button = document.querySelector(`#search-button-${i}`)
            button.textContent = `${i}` 
            button.setAttribute("onclick", `update_page(${i})`)
        }
    }else{
        for(let i = -1; i < 6; i++){
            button = document.querySelector(`#search-button-${i+2}`)
            button.textContent = `${i-2+global_id_page}` 
            button.setAttribute("onclick", `update_page(${i-2+global_id_page})`)
        }
    }
    

    var container = document.querySelector('#containers');
    container.innerHTML = ''
    max_l = data.length

    for(let i = 0; i < 10; i++){
        if (i < max_l){
            let div = document.createElement('div');
            let div_image = document.createElement('div');
            let image = document.createElement('img');
            let div_center = document.createElement('div');
            let name = document.createElement('h3');
            let game = document.createElement('h3');
            let div_button_block = document.createElement('div');
            let button_steam = document.createElement('button');
            let div_price = document.createElement('div');
            let price_buy = document.createElement('p');
            let price_profit = document.createElement('p');
            let price_sell = document.createElement('p');

            /*div.textContent = '<p>{$el}</p>';*/
            div.className = "container default-block";
            div.setAttribute("onclick", `window.location.href = "/item_${data[i].name}";`)
            div_image.className = "container-image";
            image.src = data[i].img_link + "/70fx70f";
            div_center.className = "container-center default-block";
            name.className = "item-name"
            game.className = "item-game-name"
            name.textContent = data[i].name;
            game.textContent = data[i].game;
            div_button_block.className = "button-block default-block";
            button_steam.className = "button-steam";
            button_steam.setAttribute("onclick", "window.open('" + data[i].link + "');")
            div_price.className = "price-block default-block"

            price_buy.className = "price"
            price_profit.className = "price"
            price_sell.className = "price"

            fetch(`/api/history_item_${data[i].name}`, {
                method: 'GET',
            }).then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            }).then(data => {
                price_buy.textContent = data[data.length - 1].price_buy + "$";
                price_profit.textContent = data[data.length - 1].price_profit + "$";
                price_sell.textContent = data[data.length - 1].price_sell + "$";
            }).catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });

            container.appendChild(div);
            div.appendChild(div_image);
            div.appendChild(div_center);
            div.appendChild(div_price);
            div.appendChild(div_button_block);
            
            div_image.appendChild(image);
            div_center.appendChild(name);
            div_center.appendChild(game);
            div_button_block.appendChild(button_steam);
            div_price.appendChild(price_sell);
            div_price.appendChild(price_buy);
            div_price.appendChild(price_profit);
        }
    }
}

function get_request(){

    let category = document.getElementById("category").value;
    let inputData = document.getElementById('search').value;
    fetch('/api/search', {
        method: 'POST',
        body: JSON.stringify({'data': inputData, 'id': global_id_page, "category": category}), //JSON.stringify({ data: inputData })
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        update_html(data)
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });

}


function myFunction(event) {
    if (event.key === "Enter") {
        get_request()
    }
}

function update_page(id){
    global_id_page = id
    get_request()
}

function select_request(){
    get_request()
}