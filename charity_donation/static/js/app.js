document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      // this.$form.querySelector("form").addEventListener("submit", e => this.submit_func(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      /**
       * Display only institutions containing the categories chosen in the previous step.
       */
      const c_inputs = document.getElementsByName('categories');
      const institution_label = document.querySelectorAll('#institution-label');
      const btn_1 = document.getElementById("chosen-categories");
      btn_1.addEventListener("click", e => {
        institution_label.forEach(function (i) {
          i.removeAttribute('style');
        });
        let c_checked = [];
        c_inputs.forEach(function (c) {
          if (c.checked) {
            c_checked.push(c.value);
          }
        });
        institution_label.forEach(function (i) {
          const cat = i.querySelectorAll('#cat');
          const cat_txt = [];
          cat.forEach(function (j) {
            cat_txt.push(j.textContent);
          });
          if (c_checked.every(el => cat_txt.includes(el)) === false) {
            i.style.display = 'none';
          }
        });
      });

      /**
       * Get data from inputs and show them in summary
       */
      const btn = document.getElementById('donation-confirmation');
      btn.addEventListener('click', e => {
        document.querySelectorAll(".summary--text")[0].textContent = document.getElementById('id_quantity').value;
        document.querySelectorAll(".form-section--column ul li")[0].textContent = document.getElementById('id_address').value;
        document.querySelectorAll(".form-section--column ul li")[1].textContent = document.getElementById('id_city').value;
        document.querySelectorAll(".form-section--column ul li")[2].textContent = document.getElementById('id_zip_code').value;
        document.querySelectorAll(".form-section--column ul li")[3].textContent = document.getElementById('id_phone_number').value;
        document.querySelectorAll(".form-section--column ul li")[4].textContent = document.getElementById('id_pick_up_date').value;
        document.querySelectorAll(".form-section--column ul li")[5].textContent = document.getElementById('id_pick_up_time').value;
        document.querySelectorAll(".form-section--column ul li")[6].textContent = document.getElementById('id_pick_up_comment').value;
        const i_inputs = document.getElementsByName('institution')
        i_inputs.forEach(function (i) {
          if (i.checked) {
            const institution = i.parentElement.children[2].firstElementChild.innerHTML;
            document.querySelectorAll(".summary--text")[1].textContent = "dla fundacji " + '"' + institution + '"';
          }
        })
      })

      /**
       * Display the error message if there are empty fields in the form.
       */
      const submit_prev_btn = document.getElementById("submit-prev");
      submit_prev_btn.addEventListener("click", e => {
        document.getElementById("error-msg").style.display = "none";
      });
      const submit_btn = document.getElementById("submit-btn");
      submit_btn.addEventListener("click", e => {
        if (document.querySelector("form").checkValidity() === false) {
          document.getElementById("error-msg").style.display = "inline";
        }
      });
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */

    // submit_func(e) {
    // e.preventDefault()
    // this.currentStep++;
    // this.updateForm();
    // }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
