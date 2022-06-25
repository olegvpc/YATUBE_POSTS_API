import { dataWebProjects } from "./webprojects.js";
import Project from "./Project.js";
import Section from "./Section.js";
const projectListSelector = ".web-develop__cards"

// const cardsContainer = document.querySelector(".web-develop__cards") // контейнер для web-проектов

// старая запись без использования ООП Интерфеса - Section
// function renderCard(webProjects) {
//   const newProject = new Project(webProjects, "#template-web-develop-card"); // новый экземпляр класса Card
//   cardsContainer.append(newProject.generateCard());
// }
//
// dataWebProjects.forEach(project => renderCard(project));

const sectionProjects = new Section({
  data: dataWebProjects,
  renderer: (projectItem) => {
    const project = new Project(projectItem, "#template-web-develop-card");
    const projectElement = project.generateCard();
    sectionProjects.setItem(projectElement);
  }
}, projectListSelector)

// запуск рендеринга проектов
sectionProjects.renderItems()

// анимация кнопки popup - равно в крест
const equalEx = document.querySelector(".btn-open-popup");

function handleTransform () {
  equalEx.firstChild.nextSibling.classList.toggle("x-transform");
  // console.log(equalEx);
}
equalEx.addEventListener("click", () => {
  // console.log("OPEN NAV");
  handleTransform();
  //
  openNav();
});
