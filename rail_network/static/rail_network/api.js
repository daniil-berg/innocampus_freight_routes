const api_nodes_url = '/api/nodes/';
const api_links_url = '/api/links/';
const api_shortest_path_url = '/api/shortest_path/';


async function api_request(type, api_url, request_data={}) {
  let result;
  try {
    result = await $.ajax({
      type: type,
      url: api_url,
      data: request_data,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      dataType: "json"
    });
    return result;
  } catch (e) {
    console.error(e);
  }
}

async function api_get_shortest_path(start_id, end_id, map_id = current_map_id) {
  let request_data = {
    'map': map_id,
    'start': start_id,
    'end': end_id,
  };
  return await api_request('GET', api_shortest_path_url, request_data);
}

async function api_create_node(data, map_id = current_map_id) {
  data['map'] = map_id;
  return await api_request('POST', api_nodes_url, JSON.stringify(data));
}

async function api_update_node(node_id, data, map_id = current_map_id) {
  data['map'] = map_id;
  return await api_request('PATCH', api_nodes_url + node_id + '/', JSON.stringify(data));
}

async function api_destroy_node(node_id) {
  return await api_request('DELETE', api_nodes_url + node_id + '/');
}

async function api_create_link(data, map_id = current_map_id) {
  data['map'] = map_id;
  return await api_request('POST', api_links_url, JSON.stringify(data));
}

async function api_update_link(link_id, data, map_id = current_map_id) {
  data['map'] = map_id;
  return await api_request('PATCH', api_links_url + link_id + '/', JSON.stringify(data));
}

async function api_destroy_link(link_id) {
  return await api_request('DELETE', api_links_url + link_id + '/');
}
