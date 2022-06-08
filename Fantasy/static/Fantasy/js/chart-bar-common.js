// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';
// Chart.pluginService.register({
//   afterDraw: function(chartinst) {
//     ctx = chartinst.ctx;
//     // chartinst = this;
//     this.data.datasets.forEach(function(dataset, i) {
//         if(chartinst.isDatasetVisible(i)){
//             var meta = chartinst.getDatasetMeta(i);
//             meta.data.forEach(function(bar, index) {
//                 var data = dataset.data[index];
//                 console.log(bar._model.x)
//                 console.log(bar._model.y)
//                 ctx.fillText(data, bar._model.x, bar._model.y - 2);
//             });
//         }
//     });
//   }
// })
function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
  prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
  sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
  dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
  s = '',
  toFixedFix = function(n, prec) {
    var k = Math.pow(10, prec);
    return '' + Math.round(n * k) / k;
  };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

function get_names_colors(y_data_names){
  var output = {}
  var colors_list = ["#26C6DA", "#D4E157", "#FF7043", "#BDBDBD", "#5C6BC0", "#EC407A", "#78909C", "#66BB6A", "#BA68C8", "#A1887F", "#E57373", "#455A64"]
  colors_list = colors_list.sort((a, b) => 0.5 - Math.random());
  var new_y_data_names = []
  y_data_names.forEach(e => {
    e.forEach(ee => {
      var n = ee.join(" ")
      if(!new_y_data_names.includes(n)){
        new_y_data_names.push(n)
      }
    })
  })
  index = 0
  new_y_data_names.forEach(e => {
    output[e] = colors_list[index]
    index = index + 1
  })
  y_data_colors = []
  y_data_names.forEach(e => {
    var i = []
    e.forEach(ee => {
      var n = ee.join(" ")
      i.push(output[n])
    })
    y_data_colors.push(i)
  })
  return y_data_colors
}
function set_multi_data(x_data, y_data, y_data_names, label){
  var y_data_colors = get_names_colors(y_data_names)
  y_dataset = []
  index = 0
  y_data.forEach(e => {
    y_dataset.push({
      label: label,
      backgroundColor: y_data_colors[index],
      // backgroundColor: "purple",//"#4e73df",
      // hoverBackgroundColor: "#2e59d9",
      // borderColor: "#4e73df",
      data: e,
    })
    index = index + 1
  });
  return {
    labels: x_data,
    datasets: y_dataset,
  }
}
function set_data(x_data, y_data, label, color, hover_color){
  return {
    labels: x_data,
    datasets: [{
      label: label,
      backgroundColor: color,
      hoverBackgroundColor: hover_color,
      borderColor: color,
      data: y_data,
    }],
  }
}
function set_options(y_min, y_max, x_title, y_title, x_added_label, custom_tooltip_values){
  return {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        display: true,
        position: 'bottom',
        scaleLabel: {
          display: true,
          labelString: x_title,
          fontStyle: 'bold',
          // fontSize: 12,
          // fontColor: '#030',
        },
        // time: {
        //   unit: 'month'
        // },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 6,
          callback: function(value, index, values) {
            l = (typeof x_added_label === 'undefined') ? '' : x_added_label
            if(l){
              return l + value
            }else{
              return value
            }
          }
        },
        maxBarThickness: 25,
      }],
      yAxes: [{
        display: true,
        position: 'bottom',
        scaleLabel: {
          display: true,
          labelString: y_title,
          fontStyle: 'bold',
          // fontSize: 12,
          // fontColor: '#030',
        },
        ticks: {
          min: y_min,
          max: y_max,
          maxTicksLimit: 5,
          padding: 10,
          callback: function(value, index, values) {
            return number_format(value);
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        title: function(tooltipItem, chart){
          var t = tooltipItem[0]
          var d = ''
          if(custom_tooltip_values){
            d = custom_tooltip_values[t.datasetIndex][t.index]
          }else{
            d = t.xLabel
          }
          if(Array.isArray(d)){
            d = d.join(" ")
          }
          return d
        },
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          if(datasetLabel == '%'){
            return number_format(tooltipItem.yLabel) + datasetLabel
          }else{
            return datasetLabel + ': ' + number_format(tooltipItem.yLabel);
          }
        }
      }
    },
    // animation: {
    //   duration: 0,
    //   onComplete: function() {
    //       ctx = this.ctx;
    //       chartinst = this;
    //       this.data.datasets.forEach(function(dataset, i) {
    //           if(chartinst.isDatasetVisible(i)){
    //               var meta = chartinst.getDatasetMeta(i);
    //               meta.data.forEach(function(bar, index) {
    //                   var data = dataset.data[index];
    //                   console.log(bar._model.x)
    //                   console.log(bar._model.y)
    //                   ctx.fillText(data, bar._model.x, bar._model.y - 2);
    //               });
    //           }
    //       });
    //   }
    // }
  }
}

function get_max(my_list){
  var m = Math.max(...my_list)
  var my_max = 5
  if(m > 5){my_max=10}else{return my_max}
  if(m > 10){my_max=20}else{return my_max}
  if(m > 20){my_max=30}else{return my_max}
  if(m > 30){my_max=50}else{return my_max}
  if(m > 50){my_max=100}else{return my_max}
  if(m > 100){my_max=150}else{return my_max}
  if(m > 150){my_max=200}else{return my_max}
  if(m > 200){my_max=250}else{return my_max}
  if(m > 250){my_max=300}else{return my_max}
  if(m > 300){my_max=400}else{return my_max}
  if(m > 400){my_max=500}else{return my_max}
  if(m > 500){my_max=600}else{return my_max}
  if(m > 500){my_max=600}else{return my_max}
  if(m > 600){my_max=700}else{return my_max}
  if(m > 700){my_max=800}else{return my_max}
  if(m > 800){my_max=900}else{return my_max}
  if(m > 900){my_max=1000}else{return my_max}
}
