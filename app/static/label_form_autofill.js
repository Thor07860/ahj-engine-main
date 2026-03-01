/**
 * Label Form Auto-Population
 * When a label is selected via label_number dropdown, auto-populate:
 * - UPC Code
 * - Length
 * - Width
 * - Label Name
 * - Description
 */

document.addEventListener('DOMContentLoaded', function() {
    // Find label number and UPC code select elements
    const labelNumberSelect = document.querySelector('select[name="label_number"]');
    const upcCodeSelect = document.querySelector('select[name="upc_code"]');
    const lengthInput = document.querySelector('input[name="length"]');
    const widthInput = document.querySelector('input[name="width"]');
    const labelNameSelect = document.querySelector('select[name="label_name"]');
    const descriptionInput = document.querySelector('textarea[name="description"]');
    
    if (!labelNumberSelect) {
        console.log('Label number select not found');
        return;
    }
    
    // Store original label data from select options
    const labelData = {};
    
    // Extract data from option data attributes
    Array.from(labelNumberSelect.options).forEach(option => {
        if (option.value && option.value !== '') {
            // Get the label ID from the option if available, or use the value
            labelData[option.value] = {
                text: option.textContent,
                value: option.value
            };
        }
    });
    
    console.log('Label data loaded:', labelData);
    
    // Handle label number selection
    labelNumberSelect.addEventListener('change', async function() {
        const selectedLabelNumber = this.value;
        
        if (!selectedLabelNumber || selectedLabelNumber === '') {
            // Clear fields if no selection
            clearFormFields();
            return;
        }
        
        try {
            // Find the label by label_number by searching through database
            const response = await fetch(`/api/v1/label/?skip=0&limit=500`);
            if (!response.ok) {
                console.error('Failed to fetch labels');
                return;
            }
            
            const labels = await response.json();
            const selectedLabel = labels.find(l => l.label_number === selectedLabelNumber);
            
            if (selectedLabel) {
                populateFormFields(selectedLabel);
            }
        } catch (error) {
            console.error('Error fetching label:', error);
        }
    });
    
    // Handle UPC code selection
    if (upcCodeSelect) {
        upcCodeSelect.addEventListener('change', async function() {
            const selectedUPC = this.value;
            
            if (!selectedUPC || selectedUPC === '') {
                clearFormFields();
                return;
            }
            
            try {
                const response = await fetch(`/api/v1/label/by-upc/${selectedUPC}/details`);
                if (response.ok) {
                    const label = await response.json();
                    populateFormFields(label);
                    // Also set the label_number select to match
                    if (labelNumberSelect && label.label_number) {
                        labelNumberSelect.value = label.label_number;
                    }
                }
            } catch (error) {
                console.error('Error fetching label by UPC:', error);
            }
        });
    }
    
    function populateFormFields(label) {
        console.log('Populating form with:', label);
        
        if (lengthInput) {
            lengthInput.value = label.length || '';
        }
        
        if (widthInput) {
            widthInput.value = label.width || '';
        }
        
        if (labelNameSelect && label.label_name) {
            // Find option with matching text/value
            const matchingOption = Array.from(labelNameSelect.options).find(
                opt => opt.value === label.label_name || opt.textContent.trim() === label.label_name
            );
            if (matchingOption) {
                labelNameSelect.value = matchingOption.value;
            } else {
                labelNameSelect.value = '';
            }
        }
        
        if (descriptionInput && label.description) {
            descriptionInput.value = label.description;
            // Trigger change event for CKEditor if it exists
            if (CKEDITOR && CKEDITOR.instances['description']) {
                CKEDITOR.instances['description'].setData(label.description);
            }
        }
        
        if (upcCodeSelect && label.upc_code) {
            const matchingUPCOption = Array.from(upcCodeSelect.options).find(
                opt => opt.value === label.upc_code
            );
            if (matchingUPCOption) {
                upcCodeSelect.value = label.upc_code;
            } else {
                upcCodeSelect.value = '';
            }
        }
    }
    
    function clearFormFields() {
        if (lengthInput) lengthInput.value = '';
        if (widthInput) widthInput.value = '';
        if (labelNameSelect) labelNameSelect.value = '';
        if (descriptionInput) descriptionInput.value = '';
        if (upcCodeSelect) upcCodeSelect.value = '';
    }
});
