export default class Project {
  constructor(data, templateSelector) {
    this._description = data.description;
    this._link = data.link;
    this._image = data.image;
    this._templateSelector = templateSelector;
  }
  // создание клона новой Card из шаблона
  _getTemplate() {
    return document
        .querySelector(this._templateSelector)
        .content
        .querySelector(".web-develop__card")
        .cloneNode(true);
  }
  generateCard() {
    this._cardElement = this._getTemplate();
    // console.log(this._cardElement);
    this._cardImage = this._cardElement.querySelector('.web-develop__card-img');
    this._cardLink = this._cardElement.querySelector('.web-develop__link');
    this._cardTitle = this._cardElement.querySelector('.web-develop__card-description');

    this._cardImage.src = this._image;
    this._cardImage.alt = this._description;
    this._cardLink.href =this._link;
    this._cardTitle.textContent = this._description;

    return this._cardElement;
  }
}