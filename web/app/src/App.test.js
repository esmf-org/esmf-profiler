import { render, screen } from '@testing-library/react';
import Report from "./components/Card"


test('renders learn react link', () => {
  render(<Card />);
  const linkElement = screen.getByText(/esmf/i);
  expect(linkElement).toBeInTheDocument();
});
