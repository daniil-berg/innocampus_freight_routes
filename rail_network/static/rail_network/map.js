const add_city_btn = document.getElementById('add-city');
const add_link_btn = document.getElementById('add-link');
const shortest_path_btn = document.getElementById('get-shortest-path');

const cancel_btn_class = 'cancel';
const cancel_btn_text = 'Cancel';

const add_city_btn_text = 'Add city';
const city_name_form_class = 'city-name-form';
const city_name_input_class = 'city-name-input';
const confirm_city_name_btn_class = 'confirm-city-name';

const add_link_btn_text = 'Add link';
const link_dist_form_class = 'link-dist-form';
const link_dist_input_class = 'link-dist-input';
const confirm_link_dist_btn_class = 'confirm-link-dist';

const options_wrapper_div_class = 'options-wrapper';
const confirm_node_rename_btn_class = 'confirm-node-rename';
const delete_node_btn_class = 'node-delete';

const shortest_path_btn_text = 'Get shortest path';
const algorithm_select_class = 'algorithm-select';
const algorithm_start_btn_class = 'algorithm-start';

const link_dist_attr = 'weight';

const node_default_style = {
  'width': '20px',
  'height': '20px',
  'background-color': '#666',
  'border-width': '0px',
  'label': 'data(label)',
  'font-size': '12px',
};
const node_highlight_style = {
  'background-color': '#ff0000',
  'border-width': '2px',
  'border-style': 'solid',
  'border-color': 'green',
};
const link_default_style = {
  'width': 3,
  'line-color': '#ccc',
  'label': `data(${link_dist_attr})`,
  'font-size': '12px',
};
const link_highlight_style = {
  'line-color': '#ff0000',
};

let add_node_mode = false;
let new_node = null;
let add_link_mode = false;
let new_link = null;
let new_link_start = null;
let shortest_path_mode = false;
let shortest_path_start = null;

let cy = null;

$(document).ready(function(){setup()});

function is_numeric(value) {
    return !isNaN(value - parseFloat(value));
}

function setup() {
  cy = cytoscape({
    container: document.getElementById('map'),
    elements: JSON.parse(document.getElementById('init-elements').textContent),
    style: [
      {
        selector: 'node',
        style: node_default_style
      },
      {
        selector: 'edge',
        style: link_default_style
      }
    ],
    layout: {
      name: 'preset',
      directed: false,
    }
  });

  if (cy.nodes().length > 1) { enable_link_add() }

  cy.on('tap', function(event){ if (event.target === cy) {canvas_tapped(event)} });
  cy.on('tap', 'node', function(event){node_tapped(event)});
  cy.on('add', 'node', function(){node_added()});
  cy.on('remove', 'node', function(){node_removed()});
  cy.on('dragfreeon', 'node', function(event){node_pos_change(event)});
  cy.on('tap', 'edge', function(event){link_tapped(event)});

  add_city_btn.addEventListener('click', add_city_btn_click, false);
  add_link_btn.addEventListener('click', add_link_btn_click, false);
  shortest_path_btn.addEventListener('click', shortest_path_btn_click, false);
}

function enable_link_add() {
  add_link_btn.removeAttribute('disabled');
}

function disable_link_add() {
  add_link_btn.disabled = true;
}

function canvas_tapped(event) {
  if (add_node_mode === true) {
    new_node = place_node(event.position.x, event.position.y);
    show_city_name_input(new_node);
  }
  destroy_options();
}

function node_tapped(event) {
  let node = event.target;
  if (add_link_mode === true) {
    if (new_link_start) {
      let link = create_link(node);
      show_link_dist_input(link);
    } else {
      node.style(node_highlight_style);
      new_link_start = node;
      alert_from_top('Select link END (click/tap on city node)', 2000)
    }
  } else if (shortest_path_mode === true) {
    if (shortest_path_start) {
      show_shortest_path_options(node);
    } else {
      node.style(node_highlight_style);
      shortest_path_start = node;
      alert_from_top('Select path END (click/tap on city node)', 2000)
    }
  } else {
    open_node_options(node);
  }
}

function node_added() {
  if (cy.nodes().length > 1) { enable_link_add() }
}

function node_removed() {
  if (cy.nodes().length < 2) { disable_link_add(); }
}

function node_pos_change(event) {
  let node = event.target;
  let pk = node.data('id').slice(1);  // because the first character is the "n" marker for nodes
  api_update_node(pk, node_api_data(node)).then();
}

function link_tapped(event) {
  let link = event.target;
  open_link_options(link);
}

////////////////////
// Button clicks: //
function add_city_btn_click() {
  if (add_node_mode === false) {
    add_node_mode = true;
    add_city_btn.innerText = cancel_btn_text;
    add_city_btn.setAttribute('class', cancel_btn_class);
    alert_from_top('Click/tap canvas to place new city node', 2000)
  } else {
    cancel_add_node_mode();
    if (new_node !== null) {
      new_node.remove();
    }
  }
}

function add_link_btn_click() {
  if (add_link_mode === false) {
    add_link_mode = true;
    add_link_btn.innerText = cancel_btn_text;
    add_link_btn.setAttribute('class', cancel_btn_class);
    alert_from_top('Select link START (click/tap on city node)', 2000)
  } else {
    cancel_add_link_mode();
    if (new_link !== null) {
      new_link.remove();
    }
  }
}

function shortest_path_btn_click() {
  if (shortest_path_mode === false) {
    shortest_path_mode = true;
    shortest_path_btn.innerText = cancel_btn_text;
    shortest_path_btn.setAttribute('class', cancel_btn_class);
    alert_from_top('Select path START (click/tap on city node)', 2000)
  } else {
    cancel_shortest_path_mode();
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
  let options_div = create_options_wrapper(link.renderedMidpoint());
  let input_form = create_link_dist_form();
  let input_field = create_link_dist_input();
  input_form.appendChild(input_field);
  input_form.appendChild(create_link_dist_confirm_btn(link));
  options_div.appendChild(input_form);
  document.getElementsByTagName('main')[0].appendChild(options_div);
  input_field.focus();
}

function cancel_add_link_mode() {
  add_link_mode = false;
  add_link_btn.innerText = add_link_btn_text;
  add_link_btn.removeAttribute('class');
  destroy_link_dist_input();
  cy.nodes().style(node_default_style);
}

function destroy_link_dist_input() {
  let city_name_form = document.getElementsByClassName(link_dist_form_class)[0];
  if (city_name_form) {
    city_name_form.remove();
  }
}

function open_node_options(node) {
  let options_div = create_options_wrapper(node.renderedPosition());
  let name_change_form = create_node_name_form();
  let input_field = create_node_name_input();
  name_change_form.appendChild(input_field);
  name_change_form.appendChild(create_node_change_confirm_btn(node));
  name_change_form.appendChild(create_node_delete_btn(node));
  options_div.appendChild(name_change_form);
  document.getElementsByTagName('main')[0].appendChild(options_div);
  input_field.focus();
}

function destroy_options() {
  let options_divs = document.getElementsByClassName(options_wrapper_div_class);
  for (let div of options_divs) {
    div.remove();
  }
}

function open_link_options(link) {
  let options_div = create_options_wrapper(link.renderedMidpoint());
  let link_dist_form = create_link_dist_form();
  let input_field = create_link_dist_input();
  link_dist_form.appendChild(input_field);
  link_dist_form.appendChild(create_link_dist_change_btn(link));
  link_dist_form.appendChild(create_link_delete_btn(link));
  options_div.appendChild(link_dist_form);
  document.getElementsByTagName('main')[0].appendChild(options_div);
  input_field.focus();
}

function cancel_shortest_path_mode() {
  shortest_path_mode = false;
  shortest_path_btn.innerText = shortest_path_btn_text;
  shortest_path_btn.removeAttribute('class');
  destroy_options();
  cy.nodes().style(node_default_style);
  cy.edges().style(link_default_style);
}

function show_shortest_path_options(end_node) {
  let options_div = create_options_wrapper(end_node.renderedPosition());
  let select_field = create_algorithm_select();
  options_div.appendChild(select_field);
  options_div.appendChild(create_algorithm_start_btn(end_node));
  document.getElementsByTagName('main')[0].appendChild(options_div);
}

///////////////////////////
// DOM element creation: //

function create_options_wrapper(pos) {
  let options_div = document.createElement('div');
  options_div.classList.add(options_wrapper_div_class);
  options_div.style.position = 'fixed';
  options_div.style.top = `${pos.y}px`;
  options_div.style.left = `${pos.x + 20}px`;
  return options_div;
}

function create_node_name_form() {
  let name_change_form = document.createElement('div');
  name_change_form.classList.add(city_name_form_class);
  return name_change_form;
}

function create_node_name_input() {
  let input_field = document.createElement('input');
  input_field.classList.add(city_name_input_class);
  return input_field;
}

function create_node_set_confirm_btn(node) {
  let confirm_btn = document.createElement('button');
  confirm_btn.innerHTML = "Add";
  confirm_btn.classList.add(confirm_city_name_btn_class);
  confirm_btn.setAttribute('onclick', `confirm_city_name('${node.id()}')`);
  return confirm_btn;
}

function create_node_change_confirm_btn(node) {
  let confirm_btn = document.createElement('button');
  confirm_btn.innerHTML = "Rename";
  confirm_btn.classList.add(confirm_node_rename_btn_class);
  confirm_btn.setAttribute('onclick', `change_city_name('${node.id()}')`);
  return confirm_btn;
}

function create_node_delete_btn(node) {
  let delete_btn = document.createElement('button');
  delete_btn.innerHTML = "Delete";
  delete_btn.classList.add(delete_node_btn_class);
  delete_btn.setAttribute('onclick', `delete_node_confirm(this, '${node.id()}')`);
  return delete_btn;
}

function create_link_dist_form() {
  let input_form = document.createElement('div');
  input_form.classList.add(link_dist_form_class);
  return input_form;
}

function create_link_dist_input() {
  let input_field = document.createElement('input');
  input_field.classList.add(link_dist_input_class);
  return input_field;
}

function create_link_dist_confirm_btn(link) {
  let confirm_btn = document.createElement('button');
  confirm_btn.innerHTML = "Set";
  confirm_btn.classList.add(confirm_link_dist_btn_class);
  confirm_btn.setAttribute('onclick', `confirm_link_dist('${link.data('id')}')`);
  return confirm_btn;
}

function create_link_dist_change_btn(link) {
  let confirm_btn = document.createElement('button');
  confirm_btn.innerHTML = "Set dist.";
  confirm_btn.classList.add(confirm_link_dist_btn_class);
  confirm_btn.setAttribute('onclick', `change_link_dist('${link.id()}')`);
  return confirm_btn;
}

function create_link_delete_btn(link) {
  let delete_btn = document.createElement('button');
  delete_btn.innerHTML = "Delete";
  delete_btn.classList.add(delete_node_btn_class);
  delete_btn.setAttribute('onclick', `delete_link_confirm(this, '${link.id()}')`);
  return delete_btn;
}

function create_algorithm_select() {
  let select_field = document.createElement('select');
  select_field.classList.add(algorithm_select_class);
  let option1 = document.createElement('option');
  option1.setAttribute('value', 'dijkstra');
  option1.innerHTML = "Dijkstra";
  let option2 = document.createElement('option');
  option2.setAttribute('value', 'a_star');
  option2.innerHTML = "A*";
  select_field.appendChild(option1);
  select_field.appendChild(option2);
  return select_field;
}

function create_algorithm_start_btn(end_node) {
  let confirm_btn = document.createElement('button');
  confirm_btn.innerHTML = "Start";
  confirm_btn.classList.add(algorithm_start_btn_class);
  let start = shortest_path_start.data("id");
  let end = end_node.data("id");
  confirm_btn.setAttribute('onclick', `show_shortest_path('${start}', '${end}')`);
  return confirm_btn;
}





function node_api_data(node) {
  return  {
    'pos_h': Math.round(node.position().x),
    'pos_v': Math.round(node.position().y),
    'city': {'name': node.data('label')}
  }
}

function link_api_data(link) {
  return  {
    'tail': link.data('source').slice(1),  // because the first character is the "n" marker for nodes
    'head': link.data('target').slice(1),
    'distance': link.data('weight')
  }
}




function confirm_city_name(node_id) {
  let input_value = document.getElementsByClassName(city_name_input_class)[0].value;
  let node = cy.getElementById(node_id);
  node.data('label', input_value);
  api_create_node(node_api_data(node)).then(() => window.location.reload());
  cancel_add_node_mode();
  new_node = null;
  add_node_mode = false;
}

function change_city_name(node_id) {
  let input_value = document.getElementsByClassName(city_name_input_class)[0].value;
  let node = cy.getElementById(node_id);
  node.data('label', input_value);
  let pk = node.data('id').slice(1);  // because the first character is the "n" marker for nodes
  api_update_node(pk, node_api_data(node)).then();
  destroy_options();
}

function delete_node_confirm(btn, node_id) {
  btn.innerHTML = "Confirm deletion";
  btn.setAttribute('onclick', `delete_node('${node_id}')`);
}

function delete_node(node_id) {
  let node = cy.getElementById(node_id);
  node.remove();
  let pk = node.data('id').slice(1);  // because the first character is the "n" marker for nodes
  api_destroy_node(pk).then();
  destroy_options();
}



function confirm_link_dist(link_id) {
  let input_value = document.getElementsByClassName(link_dist_input_class)[0].value;
  if (is_numeric(input_value) && input_value >= 0) {
    if (input_value < 0) {alert("Distance can not be negative"); return false}
    let link = cy.getElementById(link_id);
    link.data(link_dist_attr, input_value);
    api_create_link(link_api_data(link)).then((data) => window.location.reload());
    cancel_add_link_mode();
    new_link_start.style(node_default_style);
    link.target().style(node_default_style);
    new_link_start = null;
  } else {
    alert("Distance must be a non-negative real number")
  }
}

function change_link_dist(link_id) {
  let input_value = document.getElementsByClassName(link_dist_input_class)[0].value;
  if (is_numeric(input_value) && input_value >= 0) {
    let link = cy.getElementById(link_id);
    link.data(link_dist_attr, input_value);
    let pk = link.data('id').slice(1);  // because the first character is the "e" marker for edges
    api_update_link(pk, link_api_data(link)).then((data) => console.log(data));
    destroy_options();
  } else {
    alert("Distance must be a non-negative real number")
  }
}

function delete_link_confirm(btn, link_id) {
  btn.innerHTML = "Confirm deletion";
  btn.setAttribute('onclick', `delete_link('${link_id}')`);
}

function delete_link(link_id) {
  let link = cy.getElementById(link_id);
  link.remove();
  let pk = link.data('id').slice(1);  // because the first character is the "e" marker for edges
  api_destroy_link(pk).then();
  destroy_options();
}

async function show_shortest_path(start, end) {
  let start_id = start.slice(1);  // because the first character is the "n" marker for nodes
  let end_id = end.slice(1);
  let alg_sel = document.getElementsByClassName(algorithm_select_class)[0];
  let algorithm = alg_sel.options[alg_sel.selectedIndex].value;
  let algorithm_str = alg_sel.options[alg_sel.selectedIndex].innerText;
  const result = await api_get_shortest_path(start_id, end_id, algorithm);
  if (result['dist'] !== -1) {
    let node_labels = [];
    let prev_node_id = 'n' + start_id;
    for (let pk of result['path'].slice(1)) {
      let current_node_id = 'n' + pk;
      let node = cy.getElementById(current_node_id);
      node_labels.push(node.data('label'));
      let edge = cy.filter(`edge[source = "${prev_node_id}"][target = "${current_node_id}"]`);
      node.style(node_highlight_style);
      edge.style(link_highlight_style);
      prev_node_id = current_node_id;
    }
    alert_from_top(`Path length ${result['dist']} via ${node_labels} (Algorithm used: ${algorithm_str})`)
  } else {
    alert_from_top(`No Path exists`)
  }
  destroy_options();
  shortest_path_start = null;
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
