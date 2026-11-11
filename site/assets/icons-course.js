// A few more Tabler line icons (MIT licence, https://tabler.io/icons) for the course sites, added to the
// Helper Jobs / ASDRP icon set without changing it. Same size, stroke and class as HelperJobsIcons.
(function (root) {
  const extra = {
    "cpu": "<path d=\"M5 6a1 1 0 0 1 1 -1h12a1 1 0 0 1 1 1v12a1 1 0 0 1 -1 1h-12a1 1 0 0 1 -1 -1z\" /><path d=\"M9 9h6v6h-6z\" /><path d=\"M3 10h2\" /><path d=\"M3 14h2\" /><path d=\"M10 3v2\" /><path d=\"M14 3v2\" /><path d=\"M21 10h-2\" /><path d=\"M21 14h-2\" /><path d=\"M14 21v-2\" /><path d=\"M10 21v-2\" />",
    "stack-2": "<path d=\"M12 4l-8 4l8 4l8 -4l-8 -4\" /><path d=\"M4 12l8 4l8 -4\" /><path d=\"M4 16l8 4l8 -4\" />",
    "bolt": "<path d=\"M13 3l0 7l6 0l-8 11l0 -7l-6 0l8 -11\" />",
    "temperature": "<path d=\"M10 13.5a4 4 0 1 0 4 0v-8.5a2 2 0 0 0 -4 0v8.5\" /><path d=\"M10 9l4 0\" />",
    "server": "<path d=\"M3 7a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3z\" /><path d=\"M3 15a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3z\" /><path d=\"M7 8l0 .01\" /><path d=\"M7 16l0 .01\" />",
    "arrows-exchange": "<path d=\"M7 10h14l-4 -4\" /><path d=\"M17 14h-14l4 4\" />",
    "search": "<path d=\"M3 10a7 7 0 1 0 14 0a7 7 0 1 0 -14 0\" /><path d=\"M21 21l-6 -6\" />",
    "route": "<path d=\"M3 19a2 2 0 1 0 4 0a2 2 0 0 0 -4 0\" /><path d=\"M19 7a2 2 0 1 0 0 -4a2 2 0 0 0 0 4z\" /><path d=\"M11 19h5.5a3.5 3.5 0 0 0 0 -7h-8a3.5 3.5 0 0 1 0 -7h4.5\" />",
    "bulb": "<path d=\"M3 12h1m8 -9v1m8 8h1m-15.4 -6.4l.7 .7m12.1 -.7l-.7 .7\" /><path d=\"M9 16a5 5 0 1 1 6 0a3.5 3.5 0 0 0 -1 3a2 2 0 0 1 -4 0a3.5 3.5 0 0 0 -1 -3\" /><path d=\"M9.7 17l4.6 0\" />",
    "math-function": "<path d=\"M3 19a2 2 0 0 0 2 2c2 0 2 -4 3 -9s1 -9 3 -9a2 2 0 0 1 2 2\" /><path d=\"M5 12h6\" /><path d=\"M15 12l6 6\" /><path d=\"M15 18l6 -6\" />",
    "atom": "<path d=\"M12 12v.01\" /><path d=\"M19.071 4.929c-1.562 -1.562 -6 .337 -9.9 4.243c-3.905 3.905 -5.804 8.337 -4.242 9.9c1.562 1.561 6 -.338 9.9 -4.244c3.905 -3.905 5.804 -8.337 4.242 -9.9\" /><path d=\"M4.929 4.929c-1.562 1.562 .337 6 4.243 9.9c3.905 3.905 8.337 5.804 9.9 4.242c1.561 -1.562 -.338 -6 -4.244 -9.9c-3.905 -3.905 -8.337 -5.804 -9.9 -4.242\" />",
    "school": "<path d=\"M22 9l-10 -4l-10 4l10 4l10 -4v6\" /><path d=\"M6 10.6v5.4a6 3 0 0 0 12 0v-5.4\" />",
    "share": "<path d=\"M3 12a3 3 0 1 0 6 0a3 3 0 1 0 -6 0\" /><path d=\"M15 6a3 3 0 1 0 6 0a3 3 0 1 0 -6 0\" /><path d=\"M15 18a3 3 0 1 0 6 0a3 3 0 1 0 -6 0\" /><path d=\"M8.7 10.7l6.6 -3.4\" /><path d=\"M8.7 13.3l6.6 3.4\" />",
    "map": "<path d=\"M3 7l6 -3l6 3l6 -3v13l-6 3l-6 -3l-6 3v-13\" /><path d=\"M9 4v13\" /><path d=\"M15 7v13\" />",
    "world": "<path d=\"M3 12a9 9 0 1 0 18 0a9 9 0 0 0 -18 0\" /><path d=\"M3.6 9h16.8\" /><path d=\"M3.6 15h16.8\" /><path d=\"M11.5 3a17 17 0 0 0 0 18\" /><path d=\"M12.5 3a17 17 0 0 1 0 18\" />",
    "planet": "<path d=\"M18.816 13.58c2.292 2.138 3.546 4 3.092 4.9c-.745 1.46 -5.783 -.259 -11.255 -3.838c-5.47 -3.579 -9.304 -7.664 -8.56 -9.123c.464 -.91 2.926 -.444 5.803 .805\" /><path d=\"M7 12a5 5 0 1 0 10 0a5 5 0 1 0 -10 0\" />",
    "grid-dots": "<path d=\"M4 5a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\" /><path d=\"M11 5a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\" /><path d=\"M18 5a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\" /><path d=\"M4 12a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\" /><path d=\"M11 12a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\" /><path d=\"M18 12a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\" /><path d=\"M4 19a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\" /><path d=\"M11 19a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\" /><path d=\"M18 19a1 1 0 1 0 2 0a1 1 0 1 0 -2 0\" />",
    "affiliate": "<path d=\"M5.931 6.936l1.275 4.249m5.607 5.609l4.251 1.275\" /><path d=\"M11.683 12.317l5.759 -5.759\" /><path d=\"M4 5.5a1.5 1.5 0 1 0 3 0a1.5 1.5 0 1 0 -3 0\" /><path d=\"M17 5.5a1.5 1.5 0 1 0 3 0a1.5 1.5 0 1 0 -3 0\" /><path d=\"M17 18.5a1.5 1.5 0 1 0 3 0a1.5 1.5 0 1 0 -3 0\" /><path d=\"M4 15.5a4.5 4.5 0 1 0 9 0a4.5 4.5 0 1 0 -9 0\" />",
    "ruler": "<path d=\"M5 4h14a1 1 0 0 1 1 1v5a1 1 0 0 1 -1 1h-7a1 1 0 0 0 -1 1v7a1 1 0 0 1 -1 1h-5a1 1 0 0 1 -1 -1v-14a1 1 0 0 1 1 -1\" /><path d=\"M4 8l2 0\" /><path d=\"M4 12l3 0\" /><path d=\"M4 16l2 0\" /><path d=\"M8 4l0 2\" /><path d=\"M12 4l0 3\" /><path d=\"M16 4l0 2\" />",
    "circle-dashed": "<path d=\"M8.56 3.69a9 9 0 0 0 -2.92 1.95\" /><path d=\"M3.69 8.56a9 9 0 0 0 -.69 3.44\" /><path d=\"M3.69 15.44a9 9 0 0 0 1.95 2.92\" /><path d=\"M8.56 20.31a9 9 0 0 0 3.44 .69\" /><path d=\"M15.44 20.31a9 9 0 0 0 2.92 -1.95\" /><path d=\"M20.31 15.44a9 9 0 0 0 .69 -3.44\" /><path d=\"M20.31 8.56a9 9 0 0 0 -1.95 -2.92\" /><path d=\"M15.44 3.69a9 9 0 0 0 -3.44 -.69\" />",
    "qrcode": "<path d=\"M4 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\" /><path d=\"M7 17l0 .01\" /><path d=\"M14 5a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\" /><path d=\"M7 7l0 .01\" /><path d=\"M4 15a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v4a1 1 0 0 1 -1 1h-4a1 1 0 0 1 -1 -1z\" /><path d=\"M17 7l0 .01\" /><path d=\"M14 14l3 0\" /><path d=\"M20 14l0 .01\" /><path d=\"M14 14l0 3\" /><path d=\"M14 20l3 0\" /><path d=\"M17 17l3 0\" /><path d=\"M20 17l0 3\" />"
  };
  const base = root.HelperJobsIcons;
  function icon(name, label) {
    if (!extra[name]) return base.icon(name, label);
    return base.icon('star', label).replace(/(<svg[^>]*>).*(<\/svg>)/s, (_, open, close) => open + extra[name] + close);
  }
  root.HelperJobsIcons = { icon, names: [...base.names, ...Object.keys(extra)] };
})(window);
