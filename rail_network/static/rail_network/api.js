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

async function get_shortest_path(map_id, start_id, end_id) {
  let request_data = {
    'map': map_id,
    'start': start_id,
    'end': end_id,
  };
  return await api_request('GET', api_shortest_path_url, request_data);
}

async function update_node(map_id, node_id, data) {
  data['map'] = map_id;
  return await api_request('PATCH', api_nodes_url + node_id + '/', JSON.stringify(data));
}

async function update_link(map_id, link_id, data) {
  data['map'] = map_id;
  return await api_request('PATCH', api_links_url + link_id + '/', JSON.stringify(data));
}

$(document).ready(function(){
    // get_shortest_path(1, 1, 4).then( (data) => console.log(data));
    // update_node(1, 3, {'pos_h': 200}).then( (data) => console.log(data));
    // update_link(1, 7, {'distance': 100}).then( (data) => console.log(data));
});
