import { dataWebProjects } from "./webprojects.js";
import { dataSkills } from "./skillsData.js";
import Project from "./Project.js";
import Skill from "./Skill.js";
import Section from "./Section.js";
const projectListSelector = ".web-develop__cards"
const skillListSelector = ".skills-container"

const sectionProjects = new Section({
    data: dataWebProjects,
    renderer: (projectItem) => {
      const project = new Project(projectItem, "#template-web-develop-card");
      const projectElement = project.generateCard();
      sectionProjects.setItem(projectElement);
  }
}, projectListSelector)

const sectionSkills = new Section({
    data: dataSkills,
    renderer: (skillItem) => {
    const skill = new Skill(skillItem, ".template-skills-element");
    const skillElement = skill.generateCard();
    sectionSkills.setItem(skillElement);
  }
}, skillListSelector)

// запуск рендеринга проектов
sectionProjects.renderItems()
sectionSkills.renderItems()

// анимация кнопки popup - равно в крест
const equalEx = document.querySelector(".btn-open-popup");
const closePopup = document.querySelector(".btn-close-popup");

function handleTransform () {
  equalEx.firstChild.nextSibling.classList.toggle("x-transform");
  // console.log(equalEx);
}
equalEx.addEventListener("click", () => {
  // console.log("OPEN NAV");
  // handleTransform();
  //
  openNav();
});
closePopup.addEventListener("click", () => {
    closeNav()
})
