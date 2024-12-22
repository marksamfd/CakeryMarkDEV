import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import FooterNav from '@/app/(customer)/components/footer';

describe('FooterNav Component', () => {
  it('renders footer with working hours', () => {
    render(<FooterNav />);
    const workingHours = screen.getByText(/WORKING HOURS/i);
    expect(workingHours).toBeInTheDocument();
  });

  it('renders footer with subscribe section', () => {
    render(<FooterNav />);
    const subscribe = screen.getByText(/Subscribe/i);
    expect(subscribe).toBeInTheDocument();
  });
});