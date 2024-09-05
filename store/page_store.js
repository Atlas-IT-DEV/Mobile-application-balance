import { makeAutoObservable } from "mobx";

class RouteStore {
  route = {};
  constructor() {
    makeAutoObservable(this);
  }
  updateRoute = (new_route) => {
    this.route = new_route;
  };
}
export default RouteStore;
