// Add GeoJSON vector to the map
var vectorSource = new ol.source.Vector({
    url: 'GEOJSON.geojson', // Path to GeoJSON
    format: new ol.format.GeoJSON({
        dataProjection: 'EPSG:3857',
        featureProjection: 'EPSG:3857'
    })
});

var vectorLayer = new ol.layer.Vector({
    source: vectorSource,
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'blue',
            width: 2
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0.1)'
        })
    })
});

map.addLayer(vectorLayer);