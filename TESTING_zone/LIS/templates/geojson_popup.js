
// Display popup on click
var select = new ol.interaction.Select({
    hitTolerance: 5,
    multi: true,
    condition: ol.events.condition.singleClick
  });
map.addInteraction(select);

var popup = new ol.Overlay.PopupFeature({
    popupClass: 'default anim',
    select: select,
    canFix: true,
    template: {
        title: 
          // 'nom',   // only display the name
          function(f) {
            return f.get('Mineral')+' ('+f.get('id')+')';
          },
        attributes: // [ 'region', 'arrond', 'cantons', 'communes', 'pop' ]
        {
          'region': { title: 'Région' },
          'arrond': { title: 'Arrondissement' },
          'cantons': { title: 'Cantons' },
          'communes': { title: 'Communes' },
          // with prefix and suffix
          'pop': { 
            title: 'Population',  // attribute's title
            before: '',           // something to add before
            format: ol.Overlay.PopupFeature.localString(),  // format as local string
            after: ' hab.'        // something to add after
          },
          // calculated attribute
          'pop2': {
            title: 'Population (kHab.)',  // attribute's title
            format: function(val, f) { 
              return Math.round(parseInt(f.get('pop'))/100).toLocaleString() + ' kHab.' 
            }
          }
          /* Using localString with a date * /
          'date': { 
            title: 'Date', 
            format: ol.Overlay.PopupFeature.localString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) 
          }
          /**/
        }
    }
});
map.addOverlay (popup);
// // Create the overlay
// var container = document.getElementById('popup');
// var content = document.getElementById('popup-content');
// var closer = document.getElementById('popup-closer');

// var overlay = new ol.Overlay({
//     element: container,
//     autoPan: true,
//     autoPanAnimation: {
//         duration: 250
//     }
// });

// map.addOverlay(overlay);

// closer.onclick = function() {
//     overlay.setPosition(undefined);
//     closer.blur();
//     return false;
// };


// // // STEP 1 define a funciton to get Mineral name from the code stored in field-table
// // function getMineralName(mineral) {
// //     switch (mineral) {
// //         case 'Amph': return 'Amphibole';
// //         case 'Ep': return 'Epidote';
// //         case 'Ap': return 'Apatite';
// //         case 'Kfs': return 'K-Feldspar';
// //         case 'Ol': return 'Olivine';
// //         case 'Pl': return 'Plagioclase';
// //         case 'Px': return 'Pyroxene';
// //         case 'Qtz': return 'Quartz';
// //         case 'Cal': return 'Calcite';
// //         case 'Ca-Si min': return 'Calc-Silicate Mineral';
// //         case 'Scap (aggr)': return 'Scapolite (aggregate)';
// //         case 'Scap': return 'Scapolite';
// //         case 'Oth': return 'Other';
// //     }

// // STEP 2 create an HTML content for the popup
// // Function for PopUp Content uncomment for other fields to be displayed

// function PopUpContent(feature) {
//     var properties = feature.getProperties();
//     var mineral = properties['Mineral']; // get the mineral code from table field
//     // var popupContent = '<b> Mineral: ' + getMineralName(mineral) + '</b>';
//     var popupContent = '<b> Mineral: ' + mineral  + '</b>';
//     // popupContent += '<br> L = ' + feature.get('L');
//     // popupContent += '<br> W = ' + feature.get('W');
//     popupContent += '<br> Orientation = ' + String(feature.get('O')).substring(0, 5) + '°';
//     // popupContent += '<br> AR = ' + feature.get('AR');
//     popupContent += '<br> Aspect Ratio = ' + String(feature.get('AsR')).substring(0, 5);
//     popupContent += '<br> Area = ' + String(feature.get('A')).substring(0, 5) + ' mm²';
//     // popupContent += '<br> E = ' + feature.get('E');
//     popupContent += '<br> Roundness = ' + String(feature.get('R')).substring(0, 5);
//     // popupContent += '<br> P = ' + feature.get('P');
//     // popupContent += '<br> C = ' + feature.get('C');
//     // popupContent += '<br> Cp = ' + feature.get('Cp');
//     popupContent += '<br> Grain Shape Index = ' + String(feature.get('GSI')).substring(0, 5);
//     // popupContent += '<br> GSF = ' + feature.get('GSF');
//     // popupContent += '<br> S = ' + feature.get('S');
//     // popupContent += '<br> EQPC = ' + feature.get('EQPC');
//     // popupContent += '<br> El = ' + feature.get('El');
//     return popupContent;
// }


// // STEP 3 Display popup on click

// map.on('singleclick', function(evt) {
//     var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
//         console.log(feature);
//         console.log('Properties:', feature.getProperties());
//         return feature;
//     });


//     if (feature) {
//         var coordinates = feature.getGeometry().getCoordinates();
//         var contentHtml = PopUpContent(feature);
//         console.log(contentHtml);
//         content.innerHTML = contentHtml;
//         overlay.setPosition(coordinates);
//     }
// });