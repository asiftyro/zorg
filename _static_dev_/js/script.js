window.addEventListener("DOMContentLoaded", (event) => {
  const isSmallScreen = window.innerWidth <= 768;
  const sidebarToggle = document.body.querySelector("#sidebarToggle");
  if (sidebarToggle) {

    if (!isSmallScreen && localStorage.getItem("bws-sidebar-toggle") === "true") {
      document.body.classList.toggle("bws-sidenav-toggled");
    }
    sidebarToggle.addEventListener("click", (event) => {
      event.preventDefault();
      document.body.classList.toggle("bws-sidenav-toggled");
      if (!isSmallScreen) {
        localStorage.setItem(
          "bws-sidebar-toggle",
          document.body.classList.contains("bws-sidenav-toggled")
        );
      }
    });
  }

  // Keep parent menus open when child is active
  document.querySelectorAll(".active").forEach((item) => {
    let parent = item.closest(".collapse");
    while (parent) {
      parent.classList.add("show");
      parent = parent.parentElement.closest(".collapse");
    }
  });

  // Enable UseBootstrapSelect for all dropdown/select
  const selectTriggerList = document.querySelectorAll("select")
  const selectList = [...selectTriggerList].map(tomSelectTriggerEl => new UseBootstrapSelect(tomSelectTriggerEl, {
    searchable: "true",
    clearable: "true",
  }));
});
