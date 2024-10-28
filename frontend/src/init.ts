const initial =
  localStorage.theme === 'dark' ||
  (!('theme' in localStorage) &&
    window.matchMedia('(prefers-color-scheme: dark)').matches)

if (initial) {
  document.documentElement.classList.add('dark')
  localStorage.setItem('theme', 'dark')
} else {
  localStorage.setItem('theme', 'light')
}
