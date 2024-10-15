class SelectMultiple {
  constructor(selectId) {
    this.select = document.getElementById(selectId);
    this.leftColumn = this.select.getElementsByClassName("data_left")[0];
    this.leftSearchBox = this.select.getElementsByClassName(
      "left_search_box"
    )[0];
    this.rightColumn = this.select.getElementsByClassName("data_right")[0];
    this.rightSearchBox = this.select.getElementsByClassName(
      "right_search_box"
    )[0];
    this.buttonsBox = this.select.getElementsByClassName("box_buttons")[0];
    this.leftColumnBackup = [...this.left];
    this.rightColumnBackup = [...this.right];
    this.form = this.select.parentElement;
    this.addEvents();
  }

  addEvents() {
    this.leftSearchBox.addEventListener("keyup", (event) => {
      this.search(event);
    });
    this.rightSearchBox.addEventListener("keyup", (event) => {
      this.search(event);
    });
    this.buttonsBox.addEventListener("click", (event) => {
      this.click(event);
    });
    this.form.addEventListener("submit", (event) => {
      this.selectedRightOptionsBeforeSubmit(event);
    });
  }

  selectedRightOptionsBeforeSubmit(event) {
    this.right.map((option) => (option.selected = true));
  }

  filter(elements, target, regEx) {
    let results = elements.filter((element) =>
      element.innerText.toLowerCase().match(regEx)
    );
    if (results.length > 0) {
      target.options.length = 0;
      results.map((option) => target.append(option));
    } else {
      target.options.length = 0;
    }
  }

  restoreOptions() {
    this.rightColumnBackup.map((option) =>
      this.rightColumn.options.add(option)
    );
    this.leftColumnBackup.map((option) => this.leftColumn.options.add(option));
  }

  search(event) {
    let targetClass = event.target.className;
    let searchTerms = event.target.value;

    let searchPattern = ".*" + searchTerms + ".*";
    let regEx = new RegExp(searchPattern, "g");

    if (searchTerms === "") {
      this.restoreOptions();
    }

    if (targetClass == "left_search_box") {
      let elements = this.left;
      this.filter(elements, this.leftColumn, regEx);
    } else {
      let elements = this.right;
      this.filter(elements, this.rightColumn, regEx);
    }
  }

  refreshCache() {
    this.leftColumnBackup = this.left;
    this.rightColumnBackup = this.right;
  }

  click(event) {
    event.preventDefault();
    let targetClass = event.target.className;
    switch (targetClass) {
      case "moveAllToRight":
        this.allOptionsToRight();
        break;
      case "moveSelectedToRight":
        let leftOptions = this.leftOptionsSelected;
        this.optionsSelectedToTheRight = leftOptions;
        break;
      case "moveSelectedToLeft":
        let rightOptions = this.rightOptionsSelected;
        this.optionsSelectedToTheLeft = rightOptions;
        break;
      case "moveAllToLeft":
        this.allOptionsToLeft();
        break;
      default:
        break;
    }
    this.refreshCache();
  }

  get rightOptionsSelected() {
    return Array.from(this.rightColumn).filter(
      (element) => element.selected == true
    );
  }

  get leftOptionsSelected() {
    return Array.from(this.leftColumn).filter(
      (element) => element.selected == true
    );
  }

  get right() {
    return [...this.rightColumn];
  }

  get left() {
    return [...this.leftColumn];
  }

  set optionsSelectedToTheLeft(options) {
    options.map((element) => this.leftColumn.options.add(element));
  }

  set optionsSelectedToTheRight(options) {
    options.map((element) => this.rightColumn.options.add(element));
  }

  allOptionsToLeft() {
    this.right.map((element) => this.leftColumn.options.add(element));
  }

  allOptionsToRight() {
    this.left.map((element) => this.rightColumn.options.add(element));
  }
}

const select1 = new SelectMultiple("multiSelect1");

