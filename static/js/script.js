// To handle form submission and avoid reload
$(document).ready(function () {
  $("#form1").submit(function (event) {
    event.preventDefault();
    // const selectedItems = $(".column-checkbox").val(); // Adjust the selector to target your dropdown
    // const uselectedItems = $(".uni").val(); // Adjust the selector to target your dropdown
    // if (selectedItems.length > 1 && uselectedItems.length > 1) {
    //     alert('Ensure proper selection.');
    //     return;  // Stop form submission
    // }
    showLoading("pltalt1");
    $.ajax({
      type: "POST",
      url: "/view",
      data: $(this).serialize(),
      success: function (response) {
        $("#fig1-container").html(response.fig1);

        hideLoading("pltalt1", (msg = "Plot 1 visualized"));
        if ($("#stats-container1").length === 0) {
          // Check if the div already exists
          $("#fig1-container").after(
            '<div id="stats-container1" class="stats-container"></div>'
          );
        }
        $("#stats-container1").html(`
                    <p>Mean: ${response.stats.mean_value}</p>
                    <p>Median: ${response.stats.median_value}</p>
                    <p>Starting Value: ${response.stats.starting_value}</p>
                    <p>Last Value: ${response.stats.last_value}</p>
                    <p>Standard Deviation: ${response.stats.std_dev}</p>
                    <p>Variance: ${response.stats.variance}</p>
                `);

        // const chck = $(".column-checkbox:checked").length;
        // console.log(chck);
        // if (chck === 2) {
        //   $("#res1").html(response.res_fig1);
        //   if ($("#res_stats1").length === 0) {
        //     // Check if the div already exists
        //     $("#res1").after(
        //       '<div id="res_stats1" class="stats-container"></div>'
        //     );
        //   }
        //   $("#res_stats1").html(`     
        //                       <p>Mean: ${response.res_stats1.mean_value}</p>
        //                       <p>Median: ${response.res_stats1.median_value}</p>
        //                       <p>Starting Value: ${response.res_stats1.starting_value}</p>
        //                       <p>Last Value: ${response.res_stats1.last_value}</p>
        //                       <p>Standard Deviation: ${response.res_stats1.std_dev}</p>
        //                       <p>Variance: ${response.res_stats1.variance}</p>
        //                   `);
        //   $("#btn-modal").show(); // Show the button
        // } else {
        //   $("#btn-modal").hide(); // Hide the button
        // }

        initializeGraphSync(); // Initialize synchronization after loading the graph
        // Set up zoom event handling
      },
    });
  });

  $("#form2").submit(function (event) {
    event.preventDefault();
    // const selectedItems = $(".column-checkbox").val(); // Adjust the selector to target your dropdown
    // const uselectedItems = $(".ucolumn-checkbox").val(); // Adjust the selector to target your dropdown
    // const plt=$('.plt').val()
    showLoading("pltalt2"); 
    $.ajax({
      type: "POST",
      url: "/view",
      data: $(this).serialize(),
      success: function (response) {
        $("#fig2-container").html(response.fig2);
        hideLoading("pltalt2");

        if ($("#stats-container2").length === 0) {
          // Check if the div already exists
          $("#fig2-container").after(
            '<div id="stats-container2" class="stats-container"></div>'
          );
        }
        $("#stats-container2").html(`
                    <p>Mean: ${response.stats.mean_value}</p>
                    <p>Median: ${response.stats.median_value}</p>
                    <p>Starting Value: ${response.stats.starting_value}</p>
                    <p>Last Value: ${response.stats.last_value}</p>
                    <p>Standard Deviation: ${response.stats.std_dev}</p>
                    <p>Variance: ${response.stats.variance}</p>
                `);

        initializeGraphSync(); // Initialize synchronization after loading the graph
        // response.selected_columns2.forEach(function(option) {
        //     $('input[value="' + option + '"]').each(function() {
        //         // Only disable if the checkbox is not in the same dropdown from which it was selected
        //         if (!$(this).is(':checked')) {
        //             $(this).prop('disabled', true);
        //         }
        //     });
        // });
        // response.unival2.forEach(function(option) {
        //     $('input[value="' + option + '"]').each(function() {
        //         // Only disable if the checkbox is not in the same dropdown from which it was selected
        //         if (!$(this).is(':checked')) {
        //             $(this).prop('disabled', true);
        //         }
        //     });
        // });
      },
    });
  });

  $("#form3").submit(function (event) {
    event.preventDefault();
    // const selectedItems = $(".column-checkbox").val(); // Adjust the selector to target your dropdown
    // const uselectedItems = $(".uni").val(); // Adjust the selector to target your dropdown
    // if (selectedItems.length > 1 && uselectedItems.length > 1) {
    //     alert('Ensure proper selection.');
    //     return;  // Stop form submission
    // }
    showLoading("pltalt3");
    $.ajax({
      type: "POST",
      url: "/view",
      data: $(this).serialize(),
      success: function (response) {
        $("#fig3-container").html(response.fig3);
        hideLoading("pltalt3");
        if ($("#stats-container3").length === 0) {
          // Check if the div already exists
          $("#fig3-container").after(
            '<div id="stats-container3" class="stats-container"></div>'
          );
        }
        $("#stats-container3").html(`
                    <p>Mean: ${response.stats.mean_value}</p>
                    <p>Median: ${response.stats.median_value}</p>
                    <p>Starting Value: ${response.stats.starting_value}</p>
                    <p>Last Value: ${response.stats.last_value}</p>
                    <p>Standard Deviation: ${response.stats.std_dev}</p>
                    <p>Variance: ${response.stats.variance}</p>
                `);
        initializeGraphSync(); // Initialize synchronization after loading the graph
        // response.selected_columns3.forEach(function(option) {
        //     $('input[value="' + option + '"]').each(function() {
        //         // Only disable if the checkbox is not in the same dropdown from which it was selected
        //         if (!$(this).is(':checked')) {
        //             $(this).prop('disabled', true);
        //         }
        //     });
        // });
        // response.unival3.forEach(function(option) {
        //     $('input[value="' + option + '"]').each(function() {
        //         // Only disable if the checkbox is not in the same dropdown from which it was selected
        //         if (!$(this).is(':checked')) {
        //             $(this).prop('disabled', true);
        //         }
        //     });
        // });
      },
    });
  });

  $("#form4").submit(function (event) {
    event.preventDefault();
    // const selectedItems = $(".column-checkbox").val(); // Adjust the selector to target your dropdown
    // const uselectedItems = $(".uni").val(); // Adjust the selector to target your dropdown
    // if (selectedItems.length > 1 && uselectedItems.length > 1) {
    //     alert('Ensure proper selection.');
    //     return;  // Stop form submission
    // }
    showLoading("pltalt4");
    $.ajax({
      type: "POST",
      url: "/view",
      data: $(this).serialize(),
      success: function (response) {
        $("#fig4-container").html(response.fig4);
        hideLoading("pltalt4");
        if ($("#stats-container4").length === 0) {
          // Check if the div already exists
          $("#fig4-container").after(
            '<div id="stats-container4" class="stats-container"></div>'
          );
        }
        $("#stats-container4").html(`
                    <p>Mean: ${response.stats.mean_value}</p>
                    <p>Median: ${response.stats.median_value}</p>
                    <p>Starting Value: ${response.stats.starting_value}</p>
                    <p>Last Value: ${response.stats.last_value}</p>
                    <p>Standard Deviation: ${response.stats.std_dev}</p>
                    <p>Variance: ${response.stats.variance}</p>
                `);
        initializeGraphSync(); // Initialize synchronization after loading the graph

        // response.selected_columns4.forEach(function(option) {
        //     $('input[value="' + option + '"]').each(function() {
        //         // Only disable if the checkbox is not in the same dropdown from which it was selected
        //         if (!$(this).is(':checked')) {
        //             $(this).prop('disabled', true);
        //         }
        //     });
        // });
        // response.unival4.forEach(function(option) {
        //     $('input[value="' + option + '"]').each(function() {
        //         // Only disable if the checkbox is not in the same dropdown from which it was selected
        //         if (!$(this).is(':checked')) {
        //             $(this).prop('disabled', true);
        //         }
        //     });
        // });
      },
    });
  });

  $("#res1").submit(function (event) {
    event.preventDefault();
    const selectedItems = $(".column-checkbox:checked"); // Adjust the selector to target your dropdown
    console.log(selectedItems.length);
    if (selectedItems.length !== 2) {
        alert('Please select exactly two parameters.');
        return;  // Stop form submission
    }
    showLoading('pltalt4')
    $.ajax({
      type: "POST",
      url: "/residual",
      data: $(this).serialize(),
      success: function (response) {
        $("#res_fig-container").html(response.res_fig);
        $("#res1_fig-container").html(response.resi_fig);
        $('#mod_fig-container').html(response.mod_fig);
        hideLoading("pltalt4");
        // console.log(response.stats.mean_value);
        // if ($("#res_fig-container").length === 0) {
        //   // Check if the div already exists
        //   $("#res_fig-container").after(
        //     '<div id="resstats-container" class="stats-container"></div>'
        //   );
          $("#resstats-container").html(`
            <p>Mean: ${response.ogstats.mean_value}</p>
            <p>Median: ${response.ogstats.median_value}</p>
            <p>Starting Value: ${response.ogstats.starting_value}</p>
            <p>Last Value: ${response.ogstats.last_value}</p>
            <p>Standard Deviation: ${response.ogstats.std_dev}</p>
            <p>Variance: ${response.ogstats.variance}</p>
        `);
        // }
        // if ($("#res1_fig-container").length === 0) {
        //   // Check if the div already exists
        //   $("#res1_fig-container").after(
        //     '<div id="resstats1-container" class="stats-container"></div>'
        //   );
          $("#resstats1-container").html(`
            <p>Mean: ${response.resstats.mean_value}</p>
            <p>Median: ${response.resstats.median_value}</p>
            <p>Starting Value: ${response.resstats.starting_value}</p>
            <p>Last Value: ${response.resstats.last_value}</p>
            <p>Standard Deviation: ${response.resstats.std_dev}</p>
            <p>Variance: ${response.resstats.variance}</p>
        `);
        // }
        // if ($("#mod_fig-container").length === 0) {
        //   // Check if the div already exists
        //   $("#mod_fig-container").after(
        //     '<div id="modstats-container" class="stats-container"></div>'
        //   );
          $("#modstats-container").html(`
            <p>Mean: ${response.mod_dfstats.mean_value}</p>
            <p>Median: ${response.mod_dfstats.median_value}</p>
            <p>Starting Value: ${response.mod_dfstats.starting_value}</p>
            <p>Last Value: ${response.mod_dfstats.last_value}</p>
            <p>Standard Deviation: ${response.mod_dfstats.std_dev}</p>
            <p>Variance: ${response.mod_dfstats.variance}</p>
        `);
        // }
        
        // initializeGraphSync(); // Initialize synchronization after loading the graph
      },
      
    });
  });

  // $('.form-check-input').on('change', function() {
  //     let dropdownId = $(this).closest('.dropdown-menu').attr('id');
  //     $(this).attr('data-dropdown-id', dropdownId);
  // });

  // handle toggle
  $("#modeselect").change(function () {
    // Reinitialize synchronization when the toggle is changed
    initializeGraphSync();
  });
});

// handle sync zoom
function initializeGraphSync() {
  // Capture all dynamically generated graphs with class .plotly-graph-div
  var graphs = Array.from(document.querySelectorAll(".plotly-graph-div"));
  // var graphs = Array.from(document.querySelectorAll(".plotly-graph-div"));

  var toggleSync = document.getElementById("modeselect").checked;
  console.log(toggleSync);
  // Clear any previous event listeners
  graphs.forEach((graph) => {
    graph.removeAllListeners("plotly_relayout");
    graph.removeAllListeners("plotly_hover");
    graph.removeAllListeners("plotly_unhover");
  });
  if (graphs.length > 0) {
    var syncing = false;

    function syncRelayout(sourceGraph, targetGraphs, eventData) {
      if (!syncing) {
        syncing = true;
        var promises = targetGraphs.map((targetGraph) =>
          Plotly.relayout(targetGraph, eventData)
        );
        Promise.all(promises).then(function () {
          syncing = false;
        });
      }
    }
    // zoom parameter
    graphs.forEach((graph, index) => {
      graph.on("plotly_relayout", function (eventData) {
        var otherGraphs = graphs.filter((_, i) => i !== index);
        console.log("Relayout event triggered on graph " + (index + 1));
        // updateStats(eventData);
        if (eventData["xaxis.range[0]"] && eventData["xaxis.range[1]"]) {
          var range = {
            x_min: eventData["xaxis.range[0]"],
            x_max: eventData["xaxis.range[1]"],
          };
          console.log("Zoom range for graph " + (index + 1) + ":", range);
          updateStats(range, index); // Pass the range and index to identify the graph
        } else {
          updateStats(null, index); // If zoom-out, update stats for full dataset
        }
      });
    });
  }
  if (!toggleSync) {
    // Exit if synchronization is disabled
    if (graphs.length > 0) {
      var syncing = false;

      function syncRelayout(sourceGraph, targetGraphs, eventData) {
        if (!syncing) {
          syncing = true;
          var promises = targetGraphs.map((targetGraph) =>
            Plotly.relayout(targetGraph, eventData)
          );
          Promise.all(promises).then(function () {
            syncing = false;
          });
        }
      }
      // zoom parameter
      graphs.forEach((graph, index) => {
        graph.on("plotly_relayout", function (eventData) {
          var otherGraphs = graphs.filter((_, i) => i !== index);
          console.log("Relayout event triggered on graph " + (index + 1));
          // updateStats(eventData);

          syncRelayout(graph, otherGraphs, eventData);
          if (eventData["xaxis.range[0]"] && eventData["xaxis.range[1]"]) {
            var range = {
              x_min: eventData["xaxis.range[0]"],
              x_max: eventData["xaxis.range[1]"],
            };
            console.log("Zoom range for graph " + (index + 1) + ":", range);
            updateStats(range, index); // Pass the range and index to identify the graph
          } else {
            updateStats(null, index); // If zoom-out, update stats for full dataset
          }
        });
      });
    }
  } else {
    console.error("Plotly graph elements not found");
  }
}

function showLoading(id) {
  // document.getElementById(id).style.display = 'block';
  const alertBox = document.getElementById(id);
  alertBox.classList.remove("d-none"); // Show the alert
  alertBox.classList.add("show"); // Bootstrap 5 class to display the alert
}

function hideLoading(id) {
  // document.getElementById(id).style.display = 'none';
  const alertBox = document.getElementById(id);
  alertBox.classList.remove("show"); // Show the alert
  alertBox.classList.add("d-none"); // Bootstrap 5 class to display the alert
}

function tbload() {
  document.getElementById("load").style.display = "block";
}

function debounce(fn, delay) {
  let timeoutID;
  return function (...args) {
    if (timeoutID) clearTimeout(timeoutID);
    timeoutID = setTimeout(() => fn.apply(this, args), delay);
  };
}

document.querySelectorAll(".dropdown-submenu > a").forEach(function (element) {
  element.addEventListener(
    "mouseenter",
    debounce(function (e) {
      const submenu = this.nextElementSibling;
      submenu.style.display = "block";

      if (submenu.getBoundingClientRect().bottom > window.innerHeight) {
        submenu.style.top = "auto";
        submenu.style.bottom = "0";
      } else {
        submenu.style.top = "0";
        submenu.style.bottom = "auto";
      }

      if (submenu.getBoundingClientRect().right > window.innerWidth) {
        submenu.classList.add("dropdown-submenu-left");
      } else {
        submenu.classList.remove("dropdown-submenu-left");
      }
    }, 150)
  ); // Delay the hover action by 150ms

  element.addEventListener(
    "mouseleave",
    debounce(function (e) {
      const submenu = this.nextElementSibling;
      submenu.style.display = "none";
    }, 150)
  );
});

document.getElementById("uploadForm").addEventListener("submit", function () {
  document.getElementById("loading").style.display = "block";
});

let debounceTimer; // Ensure debounceTimer is defined globally

// Function to update statistics based on zoom range
function updateStats(range, graphIndex) {
  var g=[];
  $.ajax({
    type: "POST",
    url: "/update_stats",
    contentType: "application/json",
    data: JSON.stringify({
      range: range,
      graph_index: graphIndex, // Send graph index to associate stats with the correct graph
    }),

    success: function (response) {
      // Update the stats section based on graphIndex
      console.log(graphIndex);
      let statscont1 = document.getElementById("stats-container1");
      let statscont2 = document.getElementById("stats-container2");
      let statscont3 = document.getElementById("stats-container3");
      let statscont4 = document.getElementById("stats-container4");
      let ogstats = document.getElementById("resstats-container");
      let resstats = document.getElementById("resstats1-container");
      let modstats = document.getElementById("modstats-container");
     
      if (statscont1){
        g.push(statscont1);
      }
      if (statscont2){
        g.push(statscont2);
      }
      if (statscont3){
        g.push(statscont3);
      }
      if (statscont4){
        g.push(statscont4);
      }
      if (ogstats){
        g.push(ogstats);
      }
      if (resstats){
        g.push(resstats);
      }
      if (modstats){
        g.push(modstats);
      }


      var len=g.length;

      console.log(len);


      if (len===1){
        if (statscont1) {
          $("#stats-container1").html(` 
              <p>Mean: ${response.mean}</p>
              <p>Median: ${response.median}</p>
              <p>Starting Value: ${response.starting_value}</p>
              <p>Last Value: ${response.last_value}</p>
              <p>Standard Deviation: ${response.std_dev}</p>
              <p>Variance: ${response.variance}</p>
          `);
        }
        if (statscont2) {
          $("#stats-container2").html(` 
            <p>Mean: ${response.mean}</p>
            <p>Median: ${response.median}</p>
            <p>Starting Value: ${response.starting_value}</p>
            <p>Last Value: ${response.last_value}</p>
            <p>Standard Deviation: ${response.std_dev}</p>
            <p>Variance: ${response.variance}</p>
        `);
        }
        if (statscont3) { 
          $("#stats-container3").html(` 
            <p>Mean: ${response.mean}</p>
            <p>Median: ${response.median}</p>
            <p>Starting Value: ${response.starting_value}</p>
            <p>Last Value: ${response.last_value}</p>
            <p>Standard Deviation: ${response.std_dev}</p>
            <p>Variance: ${response.variance}</p>
        `);
        }
        if (statscont4) {
          $("#stats-container4").html(` 
            <p>Mean: ${response.mean}</p>
            <p>Median: ${response.median}</p>
            <p>Starting Value: ${response.starting_value}</p>
            <p>Last Value: ${response.last_value}</p>
            <p>Standard Deviation: ${response.std_dev}</p>
            <p>Variance: ${response.variance}</p>
        `);
        }
        if (ogstats) {
          $("#resstats-container").html(` 
              <p>Mean: ${response.mean}</p>
              <p>Median: ${response.median}</p>
              <p>Starting Value: ${response.starting_value}</p>
              <p>Last Value: ${response.last_value}</p>
              <p>Standard Deviation: ${response.std_dev}</p>
              <p>Variance: ${response.variance}</p>
          `);
        }
        if (resstats) {
          $("#resstats1-container").html(` 
              <p>Mean: ${response.mean}</p>
              <p>Median: ${response.median}</p>
              <p>Starting Value: ${response.starting_value}</p>
              <p>Last Value: ${response.last_value}</p>
              <p>Standard Deviation: ${response.std_dev}</p>
              <p>Variance: ${response.variance}</p>
          `);
        }
        if (modstats) {
          $("#modstats-container").html(` 
              <p>Mean: ${response.mean}</p>
              <p>Median: ${response.median}</p>
              <p>Starting Value: ${response.starting_value}</p>
              <p>Last Value: ${response.last_value}</p>
              <p>Standard Deviation: ${response.std_dev}</p>
              <p>Variance: ${response.variance}</p>
          `);
        }
 
      }
      else{
        if (response.graph_id === "graph1" && statscont1) {
          $("#stats-container1").html(` 
              <p>Mean: ${response.mean}</p>
              <p>Median: ${response.median}</p>
              <p>Starting Value: ${response.starting_value}</p>
              <p>Last Value: ${response.last_value}</p>
              <p>Standard Deviation: ${response.std_dev}</p>
              <p>Variance: ${response.variance}</p>
          `);
        }
        if (response.graph_id === "graph2" && statscont2) {
          $("#stats-container2").html(` 
            <p>Mean: ${response.mean}</p>
            <p>Median: ${response.median}</p>
            <p>Starting Value: ${response.starting_value}</p>
            <p>Last Value: ${response.last_value}</p>
            <p>Standard Deviation: ${response.std_dev}</p>
            <p>Variance: ${response.variance}</p>
        `);
        }
        if (response.graph_id === "graph3" && statscont3) {
          $("#stats-container3").html(` 
            <p>Mean: ${response.mean}</p>
            <p>Median: ${response.median}</p>
            <p>Starting Value: ${response.starting_value}</p>
            <p>Last Value: ${response.last_value}</p>
            <p>Standard Deviation: ${response.std_dev}</p>
            <p>Variance: ${response.variance}</p>
        `);
        }
        if (response.graph_id === "graph4" & statscont4) {
          $("#stats-container4").html(` 
            <p>Mean: ${response.mean}</p>
            <p>Median: ${response.median}</p>
            <p>Starting Value: ${response.starting_value}</p>
            <p>Last Value: ${response.last_value}</p>
            <p>Standard Deviation: ${response.std_dev}</p>
            <p>Variance: ${response.variance}</p>
        `);
        }
        $("#resstats-container").html(` 
          <p>Mean: ${response.mean}</p>
          <p>Median: ${response.median}</p>
          <p>Starting Value: ${response.starting_value}</p>
          <p>Last Value: ${response.last_value}</p>
          <p>Standard Deviation: ${response.std_dev}</p>
          <p>Variance: ${response.variance}</p>
      `);
        $("#resstats1-container").html(` 
          <p>Mean: ${response.mean}</p>
          <p>Median: ${response.median}</p>
          <p>Starting Value: ${response.starting_value}</p>
          <p>Last Value: ${response.last_value}</p>
          <p>Standard Deviation: ${response.std_dev}</p>
          <p>Variance: ${response.variance}</p>
      `);
        $("#modstats-container").html(` 
          <p>Mean: ${response.mean}</p>
          <p>Median: ${response.median}</p>
          <p>Starting Value: ${response.starting_value}</p>
          <p>Last Value: ${response.last_value}</p>
          <p>Standard Deviation: ${response.std_dev}</p>
          <p>Variance: ${response.variance}</p>
      `);
      }

      console.log(response);
      console.log("Stats updated for graph", graphIndex + 1, range);
    },
    error: function (error) {
      console.error("Error updating stats for graph", graphIndex + 1, error);
    },
  });
}

window.addEventListener("beforeunload", function (event) {
  console.log("refresh");
  fetch("/clear_session", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });
});


const time = new Date();
document.getElementById("foot").innerHTML =
  "Copyright, " + time.getFullYear() + " Dronetech Solutions Pvt Ltd.";
