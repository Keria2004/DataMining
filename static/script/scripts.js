const rawData = document.getElementById("ingredient-data").dataset.ingredients;
const ingredientsList = JSON.parse(rawData);

// Dropdown logic
function showDropdown() {
  document.getElementById("dropdownList").style.display = 'block';
}

function selectIngredient(ingredient) {
  const inputField = document.getElementById("ingredientInput");
  let parts = inputField.value.split(',');
  parts[parts.length - 1] = ' ' + ingredient;
  inputField.value = parts.join(',').replace(/^,/, '').trim() + ', ';
  document.getElementById("dropdownList").style.display = 'none';
}

function filterIngredients() {
  const searchValue = document.getElementById("ingredientInput").value.toLowerCase().split(',').pop().trim();
  const dropdown = document.getElementById("dropdownList");
  dropdown.innerHTML = '';

  if (searchValue.length > 0) {
    ingredientsList.forEach(ingredient => {
      if (ingredient.toLowerCase().startsWith(searchValue)) {
        const div = document.createElement('div');
        div.textContent = ingredient;
        div.onclick = () => selectIngredient(ingredient);
        dropdown.appendChild(div);
      }
    });
    dropdown.style.display = dropdown.children.length > 0 ? 'block' : 'none';
  } else {
    dropdown.style.display = 'none';
  }
}

window.addEventListener('click', function (event) {
  if (!event.target.closest('.dropdown-container')) {
    document.getElementById("dropdownList").style.display = 'none';
  }
});

// Tag suggestion logic
const tagContainer = document.getElementById('tagList');
const previewTags = ingredientsList.slice(0, 20);
const hiddenTags = ingredientsList.slice(20);

previewTags.forEach(ingredient => {
  createTag(ingredient);
});

// Logic for the "More" button
if (hiddenTags.length > 0) {
  const moreTag = document.createElement('div');
  moreTag.className = 'tag';
  moreTag.textContent = `+${hiddenTags.length} more`;
  moreTag.style.fontWeight = 'bold';
  moreTag.onclick = () => {
    // Display the remaining hidden ingredients
    hiddenTags.forEach(ingredient => createTag(ingredient));

    // Change the "More" button text to "Less" and toggle functionality
    moreTag.textContent = 'Less';
    moreTag.onclick = () => {
      // Remove the extra ingredients and reset the button
      hiddenTags.forEach(ingredient => {
        const tag = tagContainer.querySelector(`div.tag[data-ingredient="${ingredient}"]`);
        if (tag) {
          tag.remove();
        }
      });
      moreTag.textContent = `+${hiddenTags.length} more`; // Restore "More"
    };
  };
  tagContainer.appendChild(moreTag);
}

function createTag(ingredient) {
  const tag = document.createElement('div');
  tag.className = 'tag';
  tag.textContent = ingredient;
  tag.dataset.ingredient = ingredient; // Save ingredient info

  tag.onclick = () => {
    const inputField = document.getElementById("ingredientInput");
    let parts = inputField.value.trim().split(/\s+/).filter(p => p);

    if (tag.classList.contains('selected')) {
      // Remove selection → delete from input
      tag.classList.remove('selected');
      parts = parts.filter(item => item.toLowerCase() !== ingredient.toLowerCase());
    } else {
      // Add selection → add if not already present
      if (!parts.includes(ingredient)) {
        parts.push(ingredient);
      }
      tag.classList.add('selected');
    }

    inputField.value = parts.join(' ');
  };

  tagContainer.appendChild(tag);
}

function addIngredientToInput(ingredient) {
  const inputField = document.getElementById("ingredientInput");
  let parts = inputField.value.trim().split(/\s+/);

  if (!parts.includes(ingredient)) {
    parts.push(ingredient);
  }

  inputField.value = parts.join(' ');
}

