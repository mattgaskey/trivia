# Frontend - Trivia API

The backend for this Trivia app is a simple React app that queries the backend API endpoints across a series of components. You should be able to see a list of categories and questions when the app loads, filter by category, search questions by string, add new questions, delete existing questions, view answers to questions, and play a trivia game based on categories.

## Getting Setup

No additional setup is required for this part of the project, once the Docker container is running and the React image has compiled. To view the logs for this service, run:

```sh
docker logs -f trivia-frontend
```

## Improvements

The existing React app was defined using v16, which has since been replaced with v17 and v18.  New features for React include the use of React Hooks to handle state and dynamic changes to the page.  Plus, with the standardization of asynchronous `fetch()` methods in modern JavaScript, it is no longer necessary to use jQuery `ajax()` requests, or even include jQuery at all.

CSS files have been improved dramatically to better organize components on the page. Flexbox and Grid layouts are implemented to keep elements flowing properly in their containers. Clickable elements (especially those that use non-pointer HTML elements) have hover states and pointers to better direct users to their interactive nature.
