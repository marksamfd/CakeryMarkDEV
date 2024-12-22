import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import Title from '@/app/(customer)/components/title';

describe('Title Component', () => {
  it('renders title with children', () => {
    render(<Title>My Title</Title>);
    const title = screen.getByText(/My Title/i);
    expect(title).toBeInTheDocument();
  });
});