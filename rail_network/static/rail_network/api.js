const api_nodes_url = '/api/nodes/';
const api_links_url = '/api/links/';
const api_shortest_path_url = '/api/shortest_path/';


// $.ajaxSetup({
//   beforeSend: function(xhr, settings) {
//     function getCookie(name) {
//       var cookieValue = null;
//       if (document.cookie && document.cookie !== '') {
//         var cookies = document.cookie.split(';');
//         for (var i = 0; i < cookies.length; i++) {
//           var cookie = jQuery.trim(cookies[i]);
//           // Does this cookie string begin with the name we want?
//           if (cookie.substring(0, name.length + 1) === (name + '=')) {
//             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//             break;
//           }
//         }
//       }
//       return cookieValue;
//     }
//     if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
//       // Only send the token to relative URLs i.e. locally.
//       xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
//     }
//   }
// });

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

async function api_get_shortest_path(map_id, start_id, end_id) {
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

$(document).ready(function(){
  // get_shortest_path(1, 1, 4).then( (data) => console.log(data));
  // api_update_node(3, {'pos_h': 200}).then( (data) => console.log(data));
  // api_update_link(7, {'distance': 100}).then( (data) => console.log(data));
  // let node_data = {'pos_h': 400, 'pos_v': 400, 'city': {'name': 'Testcity NEW'}};
  // api_create_node(node_data).then( (data) => console.log(data));
  // api_destroy_node(5).then( (data) => console.log(data));
});
