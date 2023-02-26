export default class Skill {
  constructor(data, templateSelector) {
    this._name = data.nameSkill
    this._logo = data.logoSkill;
    this._level = data.levelSkill;
    this._description = data.description;
    this._templateSelector = templateSelector;
  }
  // создание клона нового Skill из шаблона
  _getTemplate() {
      // console.log(this._templateSelector)
    return document
        .querySelector(this._templateSelector)
        .content
        .querySelector(".skills__element")
        .cloneNode(true);
  }
  generateCard() {
    this._skillElement = this._getTemplate();
    // console.log(this._skillElement);
    this._skillElement.querySelector('.skills__logo').src = this._logo;
    this._skillElement.querySelector('.skills__logo').alt = this._name;
    this._skillElement.querySelector('.skills__line_gray').style = `width:${this._level}%`;
    // this._skillElement.querySelector('.skills__title').textContent = this._description;
    this._skillElement.querySelector('.skills__title').innerHTML = this._description;
    return this._skillElement;
  }
}