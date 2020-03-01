const add_city_btn = document.getElementById('add-city');
const add_link_btn = document.getElementById('add-link');

const cancel_btn_class = 'cancel';
const cancel_btn_text = 'Cancel';

const add_city_btn_text = 'Add city';
const city_name_form_class = 'city-name-form';
const city_name_input_class = 'city-name-input';
const confirm_city_name_btn_class = 'confirm-city-name';

const add_link_btn_text = 'Add route';
const link_dist_form_class = 'link-dist-form';
const link_dist_input_class = 'link-dist-input';
const confirm_link_dist_btn_class = 'confirm-link-dist';

const node_default_style = {
  'background-color': '#666',
  'border-width': '0px',
  'label': 'data(label)'
};
const node_highlight_style = {
  'background-color': '#ff0000',
  'border-width': '2px',
  'border-style': 'solid',
  'border-color': 'green',
};

let add_node_mode = false;
let new_node = null;
let add_link_mode = false;
let new_link = null;
let new_link_start = null;

let cy = cytoscape({
  container: document.getElementById('map'),
  elements: [
    // {data: { id: 'a' }},
    // {data: { id: 'b' }}
  ],
  style: [
    {
      selector: 'node',
      style: node_default_style
    },
    {
      selector: 'edge',
      style: {
        'width': 3,
        'line-color': '#ccc',
        'target-arrow-color': '#ccc',
        'target-arrow-shape': 'triangle',
        'label': 'data(label)'
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
    if (add_node_mode === true){
      new_node = place_node(event.position.x, event.position.y);
      add_node_mode = false;
      show_city_name_input(new_node);
    }
  } else {

  }
});

cy.on('tap', 'node', function (event) {
  let target = event.target;
  if (add_link_mode === true) {
    if (new_link_start) {
      let link = create_link(target);
      show_link_dist_input(link);
    } else {
      target.style(node_highlight_style);
      new_link_start = target;
    }
  }
});

cy.on('add', function () {
  if (cy.nodes().length > 1) {
    enable_link_add();
  }
});

cy.on('remove', function () {
  if (cy.nodes().length < 2) {
    disable_link_add();
  }
});

function enable_link_add() {
  add_link_btn.removeAttribute('disabled');
}

function disable_link_add() {
  add_link_btn.disabled = true;
}

add_city_btn.addEventListener('click', add_city_btn_click, false);
add_link_btn.addEventListener('click', add_link_btn_click, false);

function add_city_btn_click() {
  if (add_node_mode === false) {
    add_node_mode = true;
    add_city_btn.innerText = cancel_btn_text;
    add_city_btn.setAttribute('class', cancel_btn_class);
  } else {
    cancel_add_node_mode();
    if (new_node !== null) {
      new_node.remove();
    }
  }
}

function place_node(x, y) {
  return cy.add({
    group: 'nodes',
    data: {label: 'New city'},
    position: { x: x, y: y }
  });
}

function show_city_name_input(node) {
  let input_form = document.createElement('div');
  input_form.classList.add(city_name_form_class);
  input_form.style.position = 'fixed';
  input_form.style.top = `${node.renderedPosition().y}px`;
  input_form.style.left = `${node.renderedPosition().x + 20}px`;
  let input_field = document.createElement('input');
  input_field.classList.add(city_name_input_class);
  input_form.appendChild(input_field);
  let confirm_btn = document.createElement('button');
  confirm_btn.innerHTML = "Add";
  confirm_btn.classList.add(confirm_city_name_btn_class);
  confirm_btn.setAttribute('onclick', `confirm_city_name('${node.id()}')`);
  input_form.appendChild(confirm_btn);
  document.getElementsByTagName('main')[0].appendChild(input_form);
  input_field.focus();
}

function confirm_city_name(node_id) {
  let input_value = document.getElementsByClassName(city_name_input_class)[0].value;
  let node = cy.getElementById(node_id);
  node.data('label', input_value);
  cancel_add_node_mode();
  new_node = null;
}

function cancel_add_node_mode() {
  add_node_mode = false;
  add_city_btn.innerText = add_city_btn_text;
  add_city_btn.removeAttribute('class');
  destroy_city_name_input();
}

function destroy_city_name_input() {
  let city_name_form = document.getElementsByClassName(city_name_form_class)[0];
  if (city_name_form) {
    city_name_form.remove();
  }
}

function add_link_btn_click() {
  if (add_link_mode === false) {
    add_link_mode = true;
    add_link_btn.innerText = cancel_btn_text;
    add_link_btn.setAttribute('class', cancel_btn_class);
  } else {
    cancel_add_link_mode();
    if (new_link !== null) {
      new_link.remove();
    }
  }
}

function create_link(end_node) {
  if (new_link_start) {
    end_node.style(node_highlight_style);
    return cy.add({
      group: 'edges',
      data: {
        source: new_link_start.data('id'),
        target: end_node.data('id'),
        label: 'Dist.',
      },
    });
  }
}

function show_link_dist_input(link) {
  let input_form = document.createElement('div');
  input_form.classList.add(link_dist_form_class);
  input_form.style.position = 'fixed';
  input_form.style.top = `${link.renderedMidpoint().y + 15}px`;
  input_form.style.left = `${link.renderedMidpoint().x}px`;
  let input_field = document.createElement('input');
  input_field.classList.add(link_dist_input_class);
  input_form.appendChild(input_field);
  let confirm_btn = document.createElement('button');
  confirm_btn.innerHTML = "Set";
  confirm_btn.classList.add(confirm_link_dist_btn_class);
  confirm_btn.setAttribute('onclick', `confirm_link_dist('${link.data('id')}')`);
  input_form.appendChild(confirm_btn);
  document.getElementsByTagName('main')[0].appendChild(input_form);
  input_field.focus();
}

function confirm_link_dist(link_id) {
  let input_value = document.getElementsByClassName(link_dist_input_class)[0].value;
  let link = cy.getElementById(link_id);
  link.data('label', input_value);
  cancel_add_link_mode();
  new_link_start.style(node_default_style);
  link.target().style(node_default_style);
  new_link_start = null;
}

function cancel_add_link_mode() {
  add_link_mode = false;
  add_link_btn.innerText = add_link_btn_text;
  add_link_btn.removeAttribute('class');
  destroy_link_dist_input();
}

function destroy_link_dist_input() {
  let city_name_form = document.getElementsByClassName(link_dist_form_class)[0];
  if (city_name_form) {
    city_name_form.remove();
  }
}
