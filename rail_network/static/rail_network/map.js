const add_city_btn = document.getElementById('add-city');
const add_city_btn_text = 'Add city';
const cancel_btn_class = 'cancel';
const cancel_btn_text = 'Cancel';
const city_name_form_class = 'city-name-form';
const city_name_input_class = 'city-name-input';
const confirm_city_name_btn_class = 'confirm-city-name';
let add_mode = false;

let cy = cytoscape({
  container: document.getElementById('map'), // container to render in
  elements: [],
  style: [
    {
      selector: 'node',
      style: {
        'background-color': '#666',
        'label': 'data(label)'
      }
    },
    {
      selector: 'edge',
      style: {
        'width': 3,
        'line-color': '#ccc',
        'target-arrow-color': '#ccc',
        'target-arrow-shape': 'triangle'
      }
    }
  ],
  layout: {
    name: 'grid',
    rows: 1
  }
});

cy.on('tap', function(event){
  let target = event.target;
  if( target === cy ){
    if (add_mode === true){
      let new_node_id = place_node(event.position.x, event.position.y);
      add_mode = false;
      show_city_name_input(event.position.x, event.position.y, new_node_id);
    }
  } else {

  }
});

function add_city_btn_click() {
  add_mode = true;
  add_city_btn.innerText = cancel_btn_text;
  add_city_btn.setAttribute('class', cancel_btn_class);
}

function place_node(x, y) {
  let new_node = cy.add({
    group: 'nodes',
    data: {label: 'New city'},
    position: { x: x, y: y }
  });
  return new_node.data('id');
}

function show_city_name_input(x, y, node_id) {
  let input_form = document.createElement('div');
  input_form.classList.add(city_name_form_class);
  input_form.style.position = 'fixed';
  input_form.style.top = `${y}px`;
  input_form.style.left = `${x + 20}px`;
  let input_field = document.createElement('input');
  input_field.classList.add(city_name_input_class);
  input_form.appendChild(input_field);
  let confirm_btn = document.createElement('button');
  confirm_btn.innerHTML = "Add";
  confirm_btn.classList.add(confirm_city_name_btn_class);
  confirm_btn.setAttribute('onclick', `confirm_city_name('${node_id}')`);
  input_form.appendChild(confirm_btn);
  document.getElementsByTagName('main')[0].appendChild(input_form);
}

function confirm_city_name(node_id) {
  let input_value = document.getElementsByClassName(city_name_input_class)[0].value;
  console.log(input_value);
  let node = cy.getElementById(node_id);
  node.data('label', input_value);
  destroy_city_name_input();
  add_city_btn.innerText = add_city_btn_text;
  add_city_btn.removeAttribute('class');
}

function destroy_city_name_input() {
  let city_name_form = document.getElementsByClassName(city_name_form_class)[0];
  city_name_form.remove();
}
