var name_item = document.getElementById('name-item');
var game_item = document.getElementById('game-item');
var disc_item = document.getElementById('disc-item');
var img_item = document.getElementById('img-item');

var item_sell_lots = document.getElementById('item-sell-lots'); 
var item_buy_lots = document.getElementById('item-buy-lots'); 
var item_sell = document.getElementById('item-sell'); 
var item_buy = document.getElementById('item-buy'); 
var item_profit = document.getElementById('item-profit'); 

fetch('/api/history_' + window.location.pathname.replace("/", ""))
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  }).then(data => {

    let data_price_sell = []
    let data_time = []
    let data_price_buy = []
    let data_price_profit = []
    let data_sell_lots = []
    let data_buy_lots = []
    let new_data = data

    for(let i in new_data){
        data_price_sell.push(new_data[i].price_sell)
        data_price_buy.push(new_data[i].price_buy)
        data_time.push(new_data[i].timestamp.slice(0, -13))
        data_price_profit.push(new_data[i].price_profit)
        data_sell_lots.push(new_data[i].sell_lots)
        data_buy_lots.push(new_data[i].buy_lots)
    }

    item_sell_lots.innerText = "Лотов на продажу: " + data_sell_lots[data_sell_lots.length-1]
    item_buy_lots.innerText = "Запросов на покупку: " + data_buy_lots[data_buy_lots.length-1]
    item_sell.innerText = "Начальная цена: " + data_price_sell[data_price_sell.length-1] + "$"
    item_buy.innerText = "Начальная цена: " + data_price_buy[data_price_buy.length-1] + "$"
    item_profit.innerText = "Выгода: " + data_price_profit[data_price_profit.length-1] + "$"

    var ctx = document.getElementById('myChart1').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data_time,
            datasets: [{
                label: 'My First Dataset',
                data: data_price_sell,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }
            ]
        }
    });

    var ctx = document.getElementById('myChart2').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data_time,
            datasets: [
            {
                label: 'My First Dataset',
                data: data_price_buy,
                fill: false,
                borderColor: 'rgb(192, 75, 192)',
                tension: 0.1
            }]
        }
    });
    var ctx = document.getElementById('myChart3').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data_time,
            datasets: [
            {
                label: 'My First Dataset',
                data: data_price_profit,
                fill: false,
                borderColor: 'rgb(192, 75, 192)',
                tension: 0.1
            }]
        }
    });
    var ctx = document.getElementById('myChart4').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data_time,
            datasets: [
            {
                label: 'My First Dataset',
                data: data_sell_lots,
                fill: false,
                borderColor: 'rgb(192, 75, 192)',
                tension: 0.1
            }]
        }
    });
    var ctx = document.getElementById('myChart5').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data_time,
            datasets: [
            {
                label: 'My First Dataset',
                data: data_buy_lots,
                fill: false,
                borderColor: 'rgb(192, 75, 192)',
                tension: 0.1
            }]
        }
    });
    
    function sendPostRequest() {
        const inputData = document.getElementById('inputText').value;
    
        console.log(JSON.stringify({ data: inputData }))
    
        fetch('/api/test?={data: ' + String(inputData) + '}', {
            method: 'POST',
            //body: JSON.stringify({ data: inputData }),
            headers: {
                'accept': 'application/json'
            }
        })
    }
    

  }).catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });

fetch('/api/data_' + window.location.pathname.replace("/", ""))
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  }).then(data => {
    name_item.innerText = data.name;
    game_item.innerText = data.game;
    disc_item.innerText = data.disc;
    img_item.src = data.img_link + "/400fx400f";
  }).catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  });




