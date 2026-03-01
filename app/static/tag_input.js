/**
 * Tag Input System for SQLAdmin Multi-Select Fields
 * Provides a clean tag/chip UI for both custom TagWidget and native select[multiple]
 */

class TagInputManager {
  constructor(selectElement) {
    this.selectElement = selectElement;
    this.fieldId = selectElement.id;
    this.selectedValues = new Set(
      Array.from(selectElement.selectedOptions).map(opt => opt.value)
    );
    this.allOptions = Array.from(selectElement.options).map(opt => ({
      value: opt.value,
      label: opt.text
    }));
    this.filterText = '';
    
    this.init();
  }

  init() {
    // Check if wrapper exists (from custom TagWidget)
    const wrapperId = `${this.fieldId}_tag_container_wrapper`;
    this.wrapper = document.getElementById(wrapperId);
    
    // If wrapper doesn't exist (native select), create one
    if (!this.wrapper) {
      this.createWrapperForNativeSelect();
    }

    // Get container and dropdown elements
    this.container = this.wrapper.querySelector(`[data-tag-container="${this.fieldId}"]`);
    this.dropdown = this.wrapper.querySelector(`[data-tag-dropdown="${this.fieldId}"]`);
    this.searchInput = this.wrapper.querySelector(`[data-tag-search="${this.fieldId}"]`);
    this.optionsContainer = this.wrapper.querySelector(`[data-tag-items="${this.fieldId}"]`);

    if (!this.container || !this.dropdown || !this.searchInput || !this.optionsContainer) {
      console.warn(`Tag input elements not found for ${this.fieldId}`);
      return;
    }

    // Hide the original select element
    this.selectElement.style.display = 'none';

    this.renderTags();
    this.renderOptions();
    this.attachEventListeners();
  }

  createWrapperForNativeSelect() {
    // Create wrapper struct for native select elements
    this.wrapper = document.createElement('div');
    this.wrapper.className = 'tag-input-wrapper';
    this.wrapper.id = `${this.fieldId}_tag_container_wrapper`;
    
    const tag_container_id = `${this.fieldId}_tag_container`;
    
    this.wrapper.innerHTML = `
      <div class="tag-input-container" id="${tag_container_id}" data-tag-container="${this.fieldId}">
      </div>
      <div class="tag-dropdown-list" id="${tag_container_id}_dropdown" data-tag-dropdown="${this.fieldId}">
        <input type="text" class="tag-search-input" data-tag-search="${this.fieldId}" placeholder="Search and click to add...">
        <div class="tag-dropdown-items" data-tag-items="${this.fieldId}">
        </div>
      </div>
    `;
    
    // Insert wrapper before the original select
    this.selectElement.parentNode.insertBefore(this.wrapper, this.selectElement);
  }

  renderTags() {
    // Clear existing tags
    this.container.querySelectorAll('.tag').forEach(tag => tag.remove());
    
    // Add new tags
    this.selectedValues.forEach(value => {
      const option = this.allOptions.find(opt => opt.value === value);
      if (option) {
        const tag = document.createElement('div');
        tag.className = 'tag';
        tag.innerHTML = `
          ${this.escapeHtml(option.label)}
          <button type="button" class="tag-remove" data-value="${value}" title="Remove">×</button>
        `;
        
        tag.querySelector('.tag-remove').addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          this.removeTag(value);
        });
        
        this.container.appendChild(tag);
      }
    });
    
    this.updateSelectElement();
  }

  renderOptions() {
    this.optionsContainer.innerHTML = '';
    
    const filtered = this.allOptions.filter(opt =>
      opt.label.toLowerCase().includes(this.filterText.toLowerCase())
    );
    
    if (filtered.length === 0) {
      const emptyMessage = document.createElement('div');
      emptyMessage.className = 'tag-no-results';
      emptyMessage.textContent = 'No items found';
      this.optionsContainer.appendChild(emptyMessage);
      return;
    }

    filtered.forEach(option => {
      const item = document.createElement('div');
      item.className = 'tag-dropdown-item';
      if (this.selectedValues.has(option.value)) {
        item.classList.add('selected');
      }
      
      item.textContent = option.label;
      item.dataset.value = option.value;
      
      item.addEventListener('click', (e) => {
        e.preventDefault();
        this.toggleOption(option.value);
      });
      
      item.addEventListener('mouseenter', () => {
        item.classList.add('highlighted');
      });
      
      item.addEventListener('mouseleave', () => {
        item.classList.remove('highlighted');
      });
      
      this.optionsContainer.appendChild(item);
    });
  }

  toggleOption(value) {
    if (this.selectedValues.has(value)) {
      this.selectedValues.delete(value);
    } else {
      this.selectedValues.add(value);
    }
    this.renderTags();
    this.renderOptions();
  }

  removeTag(value) {
    this.selectedValues.delete(value);
    this.renderTags();
    this.renderOptions();
  }

  updateSelectElement() {
    // Update the original select element for form submission
    this.selectElement.querySelectorAll('option').forEach(opt => {
      opt.selected = this.selectedValues.has(opt.value);
    });
  }

  attachEventListeners() {
    // Show dropdown on container click
    this.container.addEventListener('click', (e) => {
      if (e.target.closest('.tag-remove')) {
        return; // Don't show dropdown when removing tags
      }
      this.dropdown.classList.add('active');
      this.searchInput.focus();
    });
    
    // Search filter
    this.searchInput.addEventListener('input', (e) => {
      this.filterText = e.target.value;
      this.renderOptions();
    });
    
    // Close dropdown on outside click
    document.addEventListener('click', (e) => {
      if (this.wrapper && !this.wrapper.contains(e.target)) {
        this.dropdown.classList.remove('active');
      }
    });

    // Keyboard navigation
    this.searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.dropdown.classList.remove('active');
      }
    });
  }

  escapeHtml(text) {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
  }
}

/**
 * Initialize all tag inputs on page load
 */
document.addEventListener('DOMContentLoaded', function() {
  // Find all select[multiple] elements (both custom and native)
  const selectElements = document.querySelectorAll('select[multiple]');
  
  selectElements.forEach(select => {
    try {
      // Skip if already initialized
      if (select.dataset.tagInitialized) {
        return;
      }
      
      new TagInputManager(select);
      select.dataset.tagInitialized = 'true';
    } catch (error) {
      console.error(`Error initializing TagInputManager for ${select.id}:`, error);
    }
  });

  // Move color fields to the bottom if they exist
  const formGroups = document.querySelectorAll('.form-group');
  const colorFields = [];
  
  formGroups.forEach(group => {
    const input = group.querySelector('input[type="color"]');
    if (input) {
      colorFields.push(group);
    }
  });

  // Move color fields to end
  if (colorFields.length > 0) {
    const parentContainer = formGroups[0]?.parentElement;
    if (parentContainer) {
      colorFields.forEach(field => {
        parentContainer.appendChild(field);
      });
    }
  }
});
