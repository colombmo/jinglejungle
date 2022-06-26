import { Injectable } from '@angular/core';
import {City } from '../models/city.model';
import {CITIES } from '../models/cities';
@Injectable({
  providedIn: 'root'
})
export class CityService {

  constructor() { }

  getCities(): City[]{
    return CITIES.slice(0);
  }
}
