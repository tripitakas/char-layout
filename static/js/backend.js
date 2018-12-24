/**
 * Added by Zhang Yungui on 2018/12/18.
 */

function showError(title, text) {
  swal({
    title: title, text: text, type: /失败|错误/.test(title) ? 'error' : 'warning',
    timer: 2000, showConfirmButton: false
  });
}
function showSuccess(title, text) {
  swal({title: title, text: text, type: 'success', timer: 1000, showConfirmButton: false});
}

var HTML_DECODE = {
  '&lt;': '<',
  '&gt;': '>',
  '&amp;': '&',
  '&nbsp;': ' ',
  '&quot;': '"'
};
// 将tornado在网页中输出的对象串转为JSON对象，toHTML为true时只做网页解码
function decodeJSON(s, toHTML) {
  s = s.replace(/&\w+;|&#(\d+);/g, function ($0, $1) {
    var c = HTML_DECODE[$0];
    if (c === undefined) {
      // Maybe is Entity Number
      if (!isNaN($1)) {
        c = String.fromCharCode(($1 === 160) ? 32 : $1);
      } else {
        // Not Entity Number
        c = $0;
      }
    }
    return c;
  });
  s = toHTML ? s : s.replace(/'/g, '"').replace(/: True/g, ': 1').replace(/: (False|None)/g, ': 0').replace(/\\/g, '/');
  return toHTML ? s : parseJSON(s);
}

function parseJSON(s) {
  try {
    return JSON.parse(s);
  }
  catch (e) {
    console.info('invalid JSON: ' + s);
  }
}


function getDistance(a, b) {
  var cx = a.x - b.x, cy = a.y - b.y;
  return Math.sqrt(cx * cx + cy * cy);
}

function getHandle(el, index) {
  var box = el.getBBox();
  var pt;

  if (!box) {
    return {};
  }
  switch (index) {
    case 0:   // left top
      pt = [box.x, box.y];
      break;
    case 1:   // right top
      pt = [box.x + box.width, box.y];
      break;
    case 2:   // right bottom
      pt = [box.x + box.width, box.y + box.height];
      break;
    case 3:   // left bottom
      pt = [box.x, box.y + box.height];
      break;
    case 4:   // top center
      pt = [box.x + box.width / 2, box.y];
      break;
    case 5:   // right center
      pt = [box.x + box.width, box.y + box.height / 2];
      break;
    case 6:   // bottom center
      pt = [box.x + box.width / 2, box.y + box.height];
      break;
    case 7:   // left center
      pt = [box.x, box.y + box.height / 2];
      break;
    default:  // center
      pt = [box.x + box.width / 2, box.y + box.height / 2];
      break;
  }

  return {x: pt[0], y: pt[1]};
}

function findBoxByPoint(boxes, pt) {
  var ret = null, dist = 1e5, d, i, j, el;
  var isInRect = function (el, tol) {
    var box = el.getBBox();
    return box && pt.x > box.x - tol &&
        pt.y > box.y - tol &&
        pt.x < box.x + box.width + tol &&
        pt.y < box.y + box.height + tol;
  };
  for (i = 0; i < boxes.length; i++) {
    el = boxes[i];
    if (el && isInRect(el, 5)) {
      for (j = 0; j < 8; j++) {
        d = getDistance(pt, getHandle(el, j));
        if (dist > d) {
          dist = d;
          ret = el;
        }
      }
    }
  }
  return ret;
}
