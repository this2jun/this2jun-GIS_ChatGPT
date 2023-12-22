var map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM()
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([126.9780, 37.5665]),
        zoom: 12
    })
});


function addSheltersToMap(shelters) {
    var vectorSource = new ol.source.Vector();

    shelters.forEach(shelter => {
        var shelterFeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([shelter.longitude, shelter.latitude])),
            name: shelter.name,
            id: shelter.id

        });


        shelterFeature.setStyle(new ol.style.Style({
            image: new ol.style.Circle({
                radius: 10,
                fill: new ol.style.Fill({color: 'red'})
            })
        }));

        vectorSource.addFeature(shelterFeature);
    });

    var vectorLayer = new ol.layer.Vector({
        source: vectorSource
    });

    map.addLayer(vectorLayer);

    map.on('singleclick', function(evt) {
        var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature) {
            return feature;
        });

        if (feature) {
            alert('대피소 ID: ' + feature.get('id') + '\n대피소명: ' + feature.get('name'));
        }
    });
}


fetch('/get_shelters')
    .then(response => response.json())
    .then(data => addSheltersToMap(data));
