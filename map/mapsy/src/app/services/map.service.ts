import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { CityService } from './city.service';
import { City, GeoJson } from '../models/city.model';
import { CITIES } from '../models/cities';
import 'leaflet-routing-machine';
import { Observable } from 'rxjs';
var apiToken = environment.MAPBOX_API_KEY;
declare var omnivore: any;
declare var L: any;
declare var gMap: any;
// LONDON  = [51.5072466571743,-0.12824806049256623]
// BERN = [46.947365, 7.448420]
const defaultCoords: number[] = [51.5072466571743,-0.12824806049256623]
const defaultZoom: number = 13

@Injectable({
  providedIn: 'root'
})
export class MapService {
  
  public pid;
  latlng: any;
  constructor() { }

  getCity() {
    return CITIES.slice(0)[0];
  }

  
  
}
