// To handle form submission and avoid reload
$(document).ready(function () {
    $('#form1').submit(function (event) {
        event.preventDefault();
        showLoading('load1');
        $.ajax({
            type: 'POST',
            url: '/view',
            data: $(this).serialize(),
            success: function (response) {
                $('#fig1-container').html(response.fig1);
                hideLoading('load1');
                initializeGraphSync(); // Initialize synchronization after loading the graph
            }
        });
    });

    $('#form2').submit(function (event) {
        event.preventDefault();
        showLoading('load2');
        $.ajax({
            type: 'POST',
            url: '/view',
            data: $(this).serialize(),
            success: function (response) {
                $('#fig2-container').html(response.fig2);
                hideLoading('load2');
                initializeGraphSync(); // Initialize synchronization after loading the graph
            }
        });
    });

    $('#form3').submit(function (event) {
        event.preventDefault();
        showLoading('load3');
        $.ajax({
            type: 'POST',
            url: '/view',
            data: $(this).serialize(),
            success: function (response) {
                $('#fig3-container').html(response.fig3);
                hideLoading('load3');
                initializeGraphSync(); // Initialize synchronization after loading the graph
            }
        });
    });

    $('#form4').submit(function (event) {
        event.preventDefault();
        showLoading('load4');
        $.ajax({
            type: 'POST',
            url: '/view',
            data: $(this).serialize(),
            success: function (response) {
                $('#fig4-container').html(response.fig4);
                hideLoading('load4');
                initializeGraphSync(); // Initialize synchronization after loading the graph
            }
        });
    });
    // handle toggle
    $('#modeselect').change(function () {
        // Reinitialize synchronization when the toggle is changed
        initializeGraphSync();
    });
});

// handle sync zoom
function initializeGraphSync() {
    var graphs = Array.from(document.querySelectorAll('.plotly-graph-div'));
    var toggleSync = document.getElementById('modeselect').checked;
    console.log(toggleSync)
    // Clear any previous event listeners
    graphs.forEach((graph) => {
        graph.removeAllListeners('plotly_relayout');
        graph.removeAllListeners('plotly_hover');
        graph.removeAllListeners('plotly_unhover');
    });
    if (!toggleSync){

        // Exit if synchronization is disabled
        if (graphs.length > 0) {
            var syncing = false;

            function syncRelayout(sourceGraph, targetGraphs, eventData) {
                if (!syncing) {
                    syncing = true;
                    var promises = targetGraphs.map(targetGraph => Plotly.relayout(targetGraph, eventData));
                    Promise.all(promises).then(function () {
                        syncing = false;
                    });
                }
            }
// zoom parameter
            graphs.forEach((graph, index) => {
                graph.on('plotly_relayout', function (eventData) {
                    var otherGraphs = graphs.filter((_, i) => i !== index);
                    console.log('Relayout event triggered on graph ' + (index + 1));
                    syncRelayout(graph, otherGraphs, eventData);
                });

                graph.on('plotly_hover', function (eventData) {
                    // Get the x value from the hover event
                    var xValue = eventData.points[0].x;
                    console.log('Hovered xValue:', xValue);

                    // Hover the same x value in the other graphs
                    graphs.forEach((targetGraph, targetIndex) => {
                        if (index !== targetIndex) {
                            // Hover effect needs x and y values. To simulate hover, use the nearest y-value in the target graph
                            var yValue = eventData.points[0].y; // or set a default value if y is not available
                            Plotly.Fx.hover(targetGraph, { xval: xValue});
                        }
                    });
                });

                graph.on('plotly_unhover', function () {
                    // Unhover all other graphs
                    graphs.forEach((targetGraph, targetIndex) => {
                        if (index !== targetIndex) {
                            Plotly.Fx.unhover(targetGraph);
                        }
                    });
                });
            });
        } 
    }
    else {
        console.error('Plotly graph elements not found');
    }
}

function showLoading(id) {
    document.getElementById(id).style.display = 'block';
}

function hideLoading(id) {
    document.getElementById(id).style.display = 'none';
}

function tbload(){
    document.getElementById('load').style.display='block'
}

function debounce(fn, delay) {
    let timeoutID;
    return function (...args) {
        if (timeoutID) clearTimeout(timeoutID);
        timeoutID = setTimeout(() => fn.apply(this, args), delay);
    };
}

document.querySelectorAll('.dropdown-submenu > a').forEach(function (element) {
    element.addEventListener('mouseenter', debounce(function (e) {
        const submenu = this.nextElementSibling;
        submenu.style.display = 'block';

        if (submenu.getBoundingClientRect().bottom > window.innerHeight) {
            submenu.style.top = 'auto';
            submenu.style.bottom = '0';
        } else {
            submenu.style.top = '0';
            submenu.style.bottom = 'auto';
        }

        if (submenu.getBoundingClientRect().right > window.innerWidth) {
            submenu.classList.add('dropdown-submenu-left');
        } else {
            submenu.classList.remove('dropdown-submenu-left');
        }
    }, 150)); // Delay the hover action by 150ms

    element.addEventListener('mouseleave', debounce(function (e) {
        const submenu = this.nextElementSibling;
        submenu.style.display = 'none';
    }, 150));
});
