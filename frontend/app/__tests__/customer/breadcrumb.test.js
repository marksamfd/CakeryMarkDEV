import '@testing-library/jest-dom';
import { render, screen, fireEvent } from '@testing-library/react';
import Breadcrumb from '@/app/(customer)/components/breadcrumb';

describe('Breadcrumb Component', () => {
    it('renders the home link', () => {
      render(<Breadcrumb title="Shop" />);
      const homeLink = screen.getByText(/Home/i);
      expect(homeLink).toBeInTheDocument();
    });
  });