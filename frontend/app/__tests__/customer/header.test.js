import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import HeaderNav from '@/app/(customer)/components/header';

describe('HeaderNav Component', () => {
  it('renders home link', () => {
    render(<HeaderNav />);
    const homeLink = screen.getByText(/Home/i);
    expect(homeLink).toBeInTheDocument();
  });

  it('renders shop link', () => {
    render(<HeaderNav />);
    const shopLink = screen.getByText(/Shop/i);
    expect(shopLink).toBeInTheDocument();
  });
});