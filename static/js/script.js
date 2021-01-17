var baseUrl = window.location.origin;
$(document).ready(function () {
  $("#mainContent").html($("#startPage").children());
  animateHeader();
});
var input_img = "";
var currentFileName = "";
var ajax = (config) => {
  return $.ajax(config);
};

let saveFile = () => {
  alert(
    "Viết hàm lưu file sau khi sửa ở đây! Lưu ý có dùng filter mới cho lưu"
  );
};

let fbShare = () => {
  alert("Share Social Network! Này dùng API! Từ từ viết");
};

let twitterShare = () => {
  alert("Share Social Network! Này dùng API! Từ từ viết");
};

let instaShare = () => {
  alert("Share Social Network! Này dùng API! Từ từ viết");
};

let startAppClick = () => {
  let screen = $("#mainContent");
  let author_div = $("#app-name-author");
  let startBtn = $("#start-btn");
  author_div.animate(
    {
      left: -530,
      opacity: 0,
    },
    {
      duration: 300,
      done: () => {
        startBtn.animate(
          {
            right: -300,
            opacity: 0,
          },
          {
            duration: 200,
            done: () => {
              screen.animate(
                { opacity: 0 },
                {
                  duration: 200,
                  done: () => {
                    screen.html($("#program").children());
                    screen.animate(
                      { opacity: 1 },
                      {
                        duration: 100,
                      }
                    );
                  },
                }
              );
            },
          }
        );
      },
    }
  );
};

let animateHeader = () => {
  let header = $("#app-header");
  window.onscroll = () => {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20)
      header.css({
        background: "white",
        "box-shadow": "0 .125rem .25rem rgba(0,0,0,.075)",
      });
    else header.css({ background: "transparent", "box-shadow": "unset" });
  };
};

let aboutClick = () => {
  $("#aboutModal").modal("show");
};

let startBlockUI = () => {
  $("#cal-loading").modal("show");
};
let stopBlockUI = () => {
  $("#cal-loading").modal("hide");
};

let handleImageUpload = () => {
  var file_data = $("#addNewFile").prop("files")[0];
  var form_data = new FormData();
  form_data.append("file", file_data);
  startBlockUI();
  $.ajax({
    url: baseUrl + "/upload", // point to server-side PHP script
    dataType: "text", // what to expect back from the PHP script, if anything
    cache: false,
    contentType: false,
    processData: false,
    data: form_data,
    type: "POST",
    success: function (data) {
      setTimeout(() => {
        stopBlockUI();
      }, 800);
      currentFileName = file_data.name;
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#root-img").attr("src", e.target.result);
        input_img = e.target.result;
      };
      reader.readAsDataURL(file_data);
    },
  });
};
let filterIdList = [-1, 0, 1, 2, 3, 4, 5, 6];

let renderFilterList = () => {
  let filterHTMLText = "";
  document.getElementById("filter-view").html(filterHTMLText);
};

let getFilter = (id) => {
  if (currentFileName == "") {
    alert("Vui lòng thêm hình ảnh");
  } else if (id != -1) {
    // let data = JSON.stringify({id: id, img: currentFileName});
    startBlockUI();
    $.ajax({
      url: baseUrl + "/getfilter?" + "id=" + id + "&image=" + currentFileName, // point to server-side PHP script
      type: "GET",
      success: function (data) {
        setTimeout(() => {
          stopBlockUI();
        }, 700);
        if (data) {
          resultPath = "static/return/" + data;
          console.log(resultPath);
          $("#result-img").attr("src", resultPath);
        }
      },
      error: () => {
        setTimeout(() => {
          stopBlockUI();
        }, 500);
        alert("Có lỗi xảy ra! Thử lại sau.");
      },
    });
  } else alert("Có lỗi xảy ra! Vui lòng thử lại.");
};

$(document).ready(function () {
  document.querySelector("#addNewFile").addEventListener("change", (event) => {
    handleImageUpload();
  });
});
