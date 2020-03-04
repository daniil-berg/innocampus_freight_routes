
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function alert_from_top(message, auto_close_ms = null) {
  let pad = document.createElement('div');
  pad.innerHTML = ' ';
  let msg_span = document.createElement('span');
  msg_span.innerHTML = message;
  let close_btn = document.createElement('span');
  close_btn.setAttribute('id', 'close-alert');
  close_btn.setAttribute('onclick', "this.parentElement.remove();");
  close_btn.innerHTML = '&times;';
  let div = document.createElement('div');
  div.setAttribute('id', 'alert-from-top');
  div.append(pad);
  div.append(msg_span);
  div.appendChild(close_btn);
  document.body.appendChild(div);
  if (auto_close_ms) {
    sleep(auto_close_ms).then(() => div.remove());
  }
}
