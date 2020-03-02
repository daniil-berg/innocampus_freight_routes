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

const node_options_div_class = 'node-options';
const node_rename_form_class = 'node-rename-form';
const node_rename_input_class = 'node-rename-input';
const confirm_node_rename_btn_class = 'confirm-node-rename';
const delete_node_btn_class = 'node-delete';

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
const link_dist_attr = 'label';

let add_node_mode = false;
let new_node = null;
let add_link_mode = false;
let new_link = null;
let new_link_start = null;

let cy = cytoscape({
  container: document.getElementById('map'),
  elements: [
    {group: 'nodes', data: {label: 'Testcity 1'}},
    {group: 'nodes', data: {label: 'Testcity 2'}},
    {group: 'nodes', data: {label: 'Testcity 3'}}
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
        'label': `data(${link_dist_attr})`
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
  if (target === cy) {
    if (add_node_mode === true) {
      new_node = place_node(event.position.x, event.position.y);
      add_node_mode = false;
      show_city_name_input(new_node);
    }
    destroy_node_options();
  }
});

cy.on('tap', 'node', function (event) {
  let node = event.target;
  if (add_link_mode === true) {
    if (new_link_start) {
      let link = create_link(node);
      show_link_dist_input(link);
    } else {
      node.style(node_highlight_style);
      new_link_start = node;
    }
  } else {
    open_node_options(node);
  }
});

cy.on('add', 'node', function () {
  if (cy.nodes().length > 1) {
    enable_link_add();
  }


});

cy.on('remove', 'node', function () {
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
  link.data(link_dist_attr, input_value);
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

function open_node_options(node) {
  let options_div = document.createElement('div');
  options_div.classList.add(node_options_div_class);
  options_div.style.position = 'fixed';
  options_div.style.top = `${node.renderedPosition().y}px`;
  options_div.style.left = `${node.renderedPosition().x + 20}px`;
  let name_change_form = document.createElement('div');
  name_change_form.classList.add(node_rename_form_class);
  let input_field = document.createElement('input');
  input_field.classList.add(node_rename_input_class);
  name_change_form.appendChild(input_field);
  let confirm_btn = document.createElement('button');
  confirm_btn.innerHTML = "Rename";
  confirm_btn.classList.add(confirm_node_rename_btn_class);
  confirm_btn.setAttribute('onclick', `change_city_name('${node.id()}')`);
  name_change_form.appendChild(confirm_btn);
  options_div.appendChild(name_change_form);
  let delete_btn = document.createElement('button');
  delete_btn.innerHTML = "Delete";
  delete_btn.classList.add(delete_node_btn_class);
  delete_btn.setAttribute('onclick', `delete_node('${node.id()}')`);
  name_change_form.appendChild(delete_btn);
  document.getElementsByTagName('main')[0].appendChild(options_div);
  input_field.focus();
}

function change_city_name(node_id) {
  let input_value = document.getElementsByClassName(node_rename_input_class)[0].value;
  let node = cy.getElementById(node_id);
  node.data('label', input_value);
  destroy_node_options();
}

function delete_node(node_id) {
  let node = cy.getElementById(node_id);
  node.remove();
  destroy_node_options();
}

function destroy_node_options() {
  let options_div = document.getElementsByClassName(node_options_div_class)[0];
  if (options_div) {
    options_div.remove();
  }
}

function get_adjacency_matrix() {
  let nodes = cy.nodes();
  let adj_mat = [];
  for (let node of nodes) {
    let row = [];
    for (let other_node of nodes) {
      let edges = node.edgesWith(other_node);
      if (edges.length === 1) {
        row.push(parseFloat(edges[0].data(link_dist_attr)));
      } else {
        row.push(0);
      }
    }
    adj_mat.push(row);
  }
  console.log(adj_mat);
}
