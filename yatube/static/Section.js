export default class Section {
  constructor({ data, renderer }, containerSelector) {
    this._renderedItems = data;
    this._renderer = renderer; // функция формирования экземпляров объектов для вставки
    this._container = document.querySelector(containerSelector);
  }
  setItem(element) {
    this._container.append(element);
  }
  clear() {
    // console.log("Clearing container")
    this._container.innerHTML = "";
    // console.log(this._container)
  }
  renderItems() {
    this.clear();

    this._renderedItems.forEach(item => {
    this._renderer(item);
    });
  }
}