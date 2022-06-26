import { Component, OnInit, AfterViewInit } from '@angular/core';
import { MapService } from '../services/map.service';
import { environment } from '../../environments/environment';
import { GeoJson } from '../models/city.model';

import { FileService } from '../services/file.service';
import 'leaflet-routing-machine';
import * as CanvasJS from '../../assets/canvasjs.min';
import { ShortPhoto } from '../models/shortphoto.model';
import { Photo } from '../models/photo.model';
var apiToken = environment.MAPBOX_API_KEY;

declare var L: any;

// LONDON  = [51.5072466571743,-0.12824806049256623]
// BERN = [46.947365, 7.448420]
const defaultCoords: number[] = [46.947365, 7.448420]
const defaultZoom: number = 13

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})


export class MapComponent implements OnInit {
  photos: any[];
  markers: GeoJson[] = [];
  emotions: any;
  categories: any;
  categoriesChart: any;
  emotionsChart: any;
  map: any;
  constructor(private mapService: MapService, private fileService: FileService) { }

  ngOnInit() {
    this.fileService.loadPhotosZurich().subscribe(res => {
      this.photos = res;
      // this.prepareGeoJson(this.photos);
      console.log(this.photos);
      this.fileService.loadPhotosBern().subscribe( res =>{
        res.forEach( p =>{
          this.photos.push(p);
          }
        )
        this.prepareGeoJson(this.photos)
        this.plotMap(this.markers);
      });
    });

  }

  plotMap(markers: GeoJson[]) {
    var parentThis = this;
    var map = L.map('map', {zoomControl:false}).setView(defaultCoords, defaultZoom);
    this.map = map;
    var pid = 0;
    map.maxZoom = 200;

    L.tileLayer('https://api.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
      maxZoom: 20,
      id: 'mapbox.dark',
      accessToken: apiToken
    }).addTo(map);


    function onMapClick(e) {
      
      map.flyTo(e.latlng);

      sound.update(e.layer.feature.properties.properties.sounds);
      parentThis.emotions = e.layer.feature.properties.properties.emotions;
      
      parentThis.categories = e.layer.feature.properties.properties.categories;
      
      parentThis.renderCategoriesChart(parentThis.categories[0]);
      parentThis.renderEmotionsChart(parentThis.emotions[0]);

    }
    

    markers.forEach(mark => {
      var styling = this.getMarkerStylingClass(null)
      if(mark.properties.properties.dominant){
      styling = this.getMarkerStylingClass(mark.properties.properties.dominant.category)
      }
      L.geoJSON(mark, {
        pointToLayer: function (feature, latlng) {
          return L.circleMarker(mark.geometry.coordinates, styling);
        }

      }).addTo(map)
        .on('click', onMapClick)
        .bindPopup("description: <br />" + mark.properties.description + "<br />" + "tags:<br />" + mark.properties.tags + "<br /> <br /> <a href= " + mark.properties.url[0]._content + ">view in flickr</a>");

    });


    var sound = L.control();

    sound.onAdd = function (map) {
      this._div = L.DomUtil.create('div', 'sound info');
      this.update();

      return this._div;
    }
    sound.update = function (sounds) {
      this._div.innerHTML = ""
      if (sounds) {
        for (var i = 0; i < sounds.length; i++)
          this._div.innerHTML += '<i style="background: ' + parentThis.getMarkerStylingClass(sounds[i].category).fillColor + ';width: 5px;height: 25px;float: left;margin-right: 8px;opacity: 0.7;"' +
            '></i> <span style = "color:white;font-size: 25px;width: 150px;">' +
            sounds[i].sound + ':  ' + sounds[i].db.toFixed() + ' dB</span><br>';
      }
      // console.log(this._div);

    }
    sound.addTo(map);
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {
      var categories = ["traffic","human","music","mechanical","nature"];
      this._div = L.DomUtil.create('div', 'legend_info');
      
      for (var i = 0; i < categories.length; i++){
          this._div.innerHTML += '<i style="background: ' + parentThis.getMarkerStylingClass(categories[i]).fillColor + ';width: 80px;height: 20px;float: left;margin-left: 4px;margin-right:0px;opacity: 0.7;text-align:center;"' +
            '> <span style = "color:black;font-size: 15px;width: 75px;">' +
            categories[i] +  '</span> </i>';
      }
      return this._div;
    }
    legend.addTo(map)
  }

  getMarkerStylingClass(dominantCategory: any) {
    var styling = {
      radius: 4,
      fillColor: "#0f0",
      color: "#000",
      border: "0",
      weight: 1,
      opacity: 0,
      fillOpacity: 0.7
    };
    if (dominantCategory) {
      if (dominantCategory == 'traffic') {
        // styling.color = "#f00";
        styling.fillColor = "#f22";
      }
      if (dominantCategory == 'nature') {
        // styling.color =  "#0f0";
        styling.fillColor = "#090"
      }
      if (dominantCategory == 'human') {
        // styling.color =  "#00f";
        styling.fillColor = "#55f";
      }
      if (dominantCategory == 'music') {
        // styling.color =  "#0ff"; 
        styling.fillColor = "#fd0"; // #fe7f9c watermelon :'(
      }
      if (dominantCategory == 'mechanical') {
        // styling.color =  "#ddd";
        styling.fillColor = "#ddd";
      }
    }
    return styling;
  }


  prepareGeoJson(photos: any[]) {

    photos.forEach(photo => {
      let mark: GeoJson = new GeoJson([photo.latitude, photo.longitude], photo);
      this.markers.push(mark);
    })
    console.log(this.markers[0])

  }
  renderCategoriesChart(categories: any) {
    CanvasJS.addColorSet("categories",['#f22','#55f','#ddd',"#fd0",'#0f0']);
    let chart = new CanvasJS.Chart("CChartContainer", {
      colorSet: "categories",
      animationEnabled: true,
      exportEnabled: true,
      dataPointWidth: 20,
      theme: 'dark1',
      width: 400,
      height: 400,
      title: {
        text: "Categories"
      },
      data: [{
        type: "column",
        dataPoints: [
          { y: categories.traffic, label: "traffic" },
          { y: categories.human, label: "human" },
          { y: categories.mechanical, label: "mechanical" },
          { y: categories.music, label: "music" },
          { y: categories.nature, label: "nature" }
        ]
      }],
      axisY:{
        maximum: 140,
        title: "decibel level"
      }
    });

    chart.render();
  }


  renderEmotionsChart(emotions: any) {
    CanvasJS.addColorSet("emotions",['#999']);
    let chart = new CanvasJS.Chart("eChartContainer", {
      colorSet: "emotions",
      animationEnabled: true,
      exportEnabled: true,
      dataPointWidth: 20,
      width: 400,
      height: 400,
      theme: 'dark1',
      title: {
        text: "Emotions"
      },
      data: [{
        type: "column",
        dataPoints: [
          { y: emotions.anger, label: "Anger" },
          { y: emotions.fear, label: "Fear" },
          { y: emotions.joy, label: "Joy" },
          { y: emotions.sadness, label: "Sadness" },
          { y: emotions.surprise, label: "Surprise" }
        ]
      }],
      axisY:{
        maximum: 1,
        title: "probability"
      }
    });

    chart.render();
  }
}

